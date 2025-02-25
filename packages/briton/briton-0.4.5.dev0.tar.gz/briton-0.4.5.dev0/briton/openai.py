import json
import logging
import random
import time
from json import JSONDecodeError
from typing import Any, AsyncGenerator, Callable, List, Literal, Optional

import openai.types.chat.chat_completion as chat_completion
import openai.types.chat.chat_completion_chunk as chat_completion_chunk
from fastapi import HTTPException
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from openai.types.chat.chat_completion_message import ChatCompletionMessage
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
    Function,
)
from openai.types.completion import Completion
from openai.types.completion_choice import CompletionChoice
from openai.types.completion_usage import CompletionUsage

from briton.async_util import interleave_generators
from briton.constants import ALPHANUMERIC_CHARS

logger = logging.getLogger(__name__)


def _load_content_json(content: str) -> Any:
    """Safely load the content json from the input text."""
    try:
        return json.loads(content)
    except JSONDecodeError:
        raise HTTPException(status_code=400, detail="Tool call was cut off by max_tokens.")


def generate_tool_call_id() -> str:
    return "".join(random.choices(ALPHANUMERIC_CHARS, k=9))


def generate_tool_call_id_vllm() -> str:
    return "chatcmpl-tool-" + "".join(random.choices(ALPHANUMERIC_CHARS, k=32))


def _create_tool_calls(
    content: str,
    tool_call_id_fn: Callable[[], str],
) -> List[ChatCompletionMessageToolCall]:
    content_json = _load_content_json(content)
    tool_calls = []
    for briton_fn in content_json:
        fn = Function(name=briton_fn["name"], arguments=json.dumps(briton_fn["parameters"]))
        tool_call = ChatCompletionMessageToolCall(
            id=tool_call_id_fn(), function=fn, type="function"
        )
        tool_calls.append(tool_call)
    return tool_calls


def _finish_reason_from_text(
    text: str, eos_token: Optional[str] = None, stop_words: Optional[List[str]] = None
) -> Literal["stop", "length"]:
    if eos_token and text.endswith(eos_token):
        return "stop"
    if stop_words and text.endswith(tuple(stop_words)):
        return "stop"
    return "length"


def remove_suffix_from_text(
    text: str,
    eos_token: Optional[str] = None,
    stop_words: Optional[List[str]] = None,
    skip_special_tokens: Optional[List[str]] = None,
) -> str:
    if eos_token and text.endswith(eos_token):
        return text.removesuffix(eos_token)
    if stop_words:
        for stop_word in stop_words:
            if text.endswith(stop_word):
                return text.removesuffix(stop_word)
    # HACK (bdubayah): this could end up being very expensive.
    if skip_special_tokens:
        for special_token in skip_special_tokens:
            text = text.replace(special_token, "")
    return text


def _create_choice(
    index: int,
    text: str,
    eos_token: Optional[str],
    tool_token: Optional[str],
    tool_call_id_fn: Optional[Callable[[], str]],
    stop_words: Optional[List[str]],
    skip_special_tokens: Optional[List[str]],
    is_chat_completion: bool,
) -> chat_completion.Choice:
    finish_reason = _finish_reason_from_text(text, eos_token, stop_words)
    content = remove_suffix_from_text(text, eos_token, stop_words, skip_special_tokens)
    if is_chat_completion:
        tool_calls = None
        if (
            tool_token is not None
            and tool_call_id_fn is not None
            and content.startswith(tool_token)
        ):
            finish_reason = "tool_calls"
            content = content.removeprefix(tool_token)
            tool_calls = _create_tool_calls(content, tool_call_id_fn)
            content = None
        message = ChatCompletionMessage(content=content, role="assistant", tool_calls=tool_calls)
        return chat_completion.Choice(finish_reason=finish_reason, index=index, message=message)
    else:
        if content is None:
            content = ""
        return CompletionChoice(finish_reason=finish_reason, index=index, text=content)


def create_completion(
    req_id: str,
    model: str,
    sequences: List[str],
    eos_token: Optional[str] = None,
    tool_token: Optional[str] = None,
    tool_call_id_fn: Optional[Callable[[], str]] = None,
    prompt_tokens: Optional[int] = None,
    completion_tokens: Optional[int] = None,
    stop_words: Optional[List[str]] = None,
    skip_special_tokens: Optional[List[str]] = None,
    is_chat_completion: bool = False,
) -> ChatCompletion:
    created = int(time.time())
    choices = []
    for i, text in enumerate(sequences):
        choice = _create_choice(
            index=i,
            text=text,
            eos_token=eos_token,
            tool_token=tool_token,
            tool_call_id_fn=tool_call_id_fn,
            stop_words=stop_words,
            skip_special_tokens=skip_special_tokens,
            is_chat_completion=is_chat_completion,
        )
        choices.append(choice)
    usage = None
    if prompt_tokens is not None and completion_tokens is not None:
        usage = CompletionUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )
    if is_chat_completion:
        return ChatCompletion(
            id=req_id,
            choices=choices,
            created=created,
            model=model,
            object="chat.completion",
            usage=usage,
        )
    else:
        return Completion(
            id=req_id,
            choices=choices,
            created=created,
            model=model,
            object="text_completion",
            usage=usage,
        )


def _make_sse_chunk(chunk: ChatCompletionChunk | Completion) -> str:
    return f"data: {chunk.model_dump_json()}\n\n"


async def _chunk_args(args_str: str) -> AsyncGenerator[str, None]:
    chunk = ""
    for char in args_str:
        chunk += char
        if char == " ":
            yield chunk
            chunk = ""
    if chunk:
        yield chunk


async def _create_tool_call_deltas(
    content: str,
    tool_call_id_fn: Callable[[], str],
) -> AsyncGenerator[chat_completion_chunk.ChoiceDeltaToolCall, None]:
    content_json = _load_content_json(content)
    for i, briton_fn in enumerate(content_json):
        if not (isinstance(briton_fn, dict) and "name" in briton_fn and "parameters" in briton_fn):
            logger.error(f"Generated tool calls {content_json} are not valid")
            continue

        name_delta = chat_completion_chunk.ChoiceDeltaToolCall(
            index=i,
            id=tool_call_id_fn(),
            function=chat_completion_chunk.ChoiceDeltaToolCallFunction(name=briton_fn["name"]),
            type="function",
        )
        yield name_delta

        args_str = json.dumps(briton_fn["parameters"])
        async for chunk in _chunk_args(args_str):
            args_delta = chat_completion_chunk.ChoiceDeltaToolCall(
                index=i,
                function=chat_completion_chunk.ChoiceDeltaToolCallFunction(arguments=chunk),
                type="function",
            )
            yield args_delta


def _create_completion_chunk(
    id: str,
    created: int,
    index: int,
    model: str,
    is_chat_completion: bool,
    content: Optional[str] = None,
    role: Optional[Literal["system", "user", "assistant", "tool"]] = None,
    finish_reason: Optional[
        Literal["stop", "length", "tool_calls", "content_filter", "function_call"]
    ] = None,
    tool_calls: Optional[List[chat_completion_chunk.ChoiceDeltaToolCall]] = None,
) -> ChatCompletionChunk | Completion:
    if is_chat_completion:
        delta = chat_completion_chunk.ChoiceDelta(content=content, role=role, tool_calls=tool_calls)
        choice = chat_completion_chunk.Choice(index=index, delta=delta, finish_reason=finish_reason)
        return ChatCompletionChunk(
            id=id,
            choices=[choice],
            created=created,
            model=model,
            object="chat.completion.chunk",
        )
    else:
        if content is None:
            content = ""
        if finish_reason is None:
            finish_reason = "length"
        choice = CompletionChoice(index=index, text=content, finish_reason=finish_reason)
        return Completion(
            id=id,
            choices=[choice],
            created=created,
            model=model,
            object="text_completion",
        )


async def _create_completion_chunks(
    created: int,
    req_id: str,
    index: int,
    model: str,
    input_text: AsyncGenerator[str, None],
    eos_token: Optional[str],
    tool_token: Optional[str],
    tool_call_id_fn: Optional[Callable[[], str]],
    stop_words: Optional[List[str]],
    skip_special_tokens: Optional[List[str]],
    is_chat_completion: bool,
) -> AsyncGenerator[ChatCompletionChunk | Completion, None]:
    start_chunk = _create_completion_chunk(
        id=req_id,
        created=created,
        index=index,
        model=model,
        content="",
        role="assistant",
        is_chat_completion=is_chat_completion,
    )
    is_first_iter = True
    delta = None
    async for delta in input_text:
        if is_first_iter:
            if tool_token is not None and delta.startswith(tool_token):
                break
            is_first_iter = False
            yield start_chunk

        content = remove_suffix_from_text(
            text=delta,
            eos_token=eos_token,
            stop_words=stop_words,
            skip_special_tokens=skip_special_tokens,
        )
        if len(content) == 0:
            continue  # Don't send empty chunks
        yield _create_completion_chunk(
            id=req_id,
            created=created,
            index=index,
            model=model,
            content=content,
            is_chat_completion=is_chat_completion,
        )

    if (
        is_first_iter
        and delta is not None
        and tool_token is not None
        and tool_call_id_fn is not None
        and delta.startswith(tool_token)
    ):
        full_text = delta.removeprefix(tool_token)
        async for delta in input_text:
            full_text += delta

        tool_calls = _create_tool_call_deltas(
            remove_suffix_from_text(
                text=full_text,
                eos_token=eos_token,
                stop_words=stop_words,
                skip_special_tokens=skip_special_tokens,
            ),
            tool_call_id_fn,
        )
        yield start_chunk
        async for tool_call_chunk in tool_calls:
            yield _create_completion_chunk(
                id=req_id,
                created=created,
                index=index,
                model=model,
                tool_calls=[tool_call_chunk],
                is_chat_completion=is_chat_completion,
            )
        finish_reason = "tool_calls"
    else:
        finish_reason = (
            _finish_reason_from_text(text=delta, eos_token=eos_token, stop_words=stop_words)
            if delta is not None
            else "length"
        )

    yield _create_completion_chunk(
        id=req_id,
        created=created,
        index=index,
        model=model,
        finish_reason=finish_reason,
        is_chat_completion=is_chat_completion,
    )


async def create_completion_chunks(
    req_id: str,
    model: str,
    sequences: List[AsyncGenerator[str, None]],
    eos_token: Optional[str] = None,
    tool_token: Optional[str] = None,
    tool_call_id_fn: Optional[Callable[[], str]] = None,
    prompt_tokens: Optional[int] = None,
    completion_tokens_fn: Optional[Callable[[], int]] = None,
    stop_words: Optional[List[str]] = None,
    skip_special_tokens: Optional[List[str]] = None,
    is_chat_completion: bool = False,
) -> AsyncGenerator[str, None]:
    created = int(time.time())

    chunk_generators = [
        _create_completion_chunks(
            created=created,
            req_id=req_id,
            index=i,
            model=model,
            input_text=input_text_gen,
            eos_token=eos_token,
            tool_token=tool_token,
            tool_call_id_fn=tool_call_id_fn,
            stop_words=stop_words,
            skip_special_tokens=skip_special_tokens,
            is_chat_completion=is_chat_completion,
        )
        for i, input_text_gen in enumerate(sequences)
    ]
    async for chunk in interleave_generators(*chunk_generators):
        yield _make_sse_chunk(chunk)

    if prompt_tokens is not None and completion_tokens_fn is not None:
        completion_tokens = completion_tokens_fn()
        usage = CompletionUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )
        if is_chat_completion:
            usage_chunk = ChatCompletionChunk(
                id=req_id,
                choices=[],
                created=created,
                model=model,
                object="chat.completion.chunk",
                usage=usage,
            )
        else:
            usage_chunk = Completion(
                id=req_id,
                choices=[],
                created=created,
                model=model,
                object="text_completion",
                usage=usage,
            )
        yield _make_sse_chunk(usage_chunk)

    yield "data: [DONE]\n\n"
