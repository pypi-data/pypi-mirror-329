from typing import Any, AsyncGenerator, Awaitable, Callable, Dict, List, Optional, Union

from briton.backend.backend_types import RequestDetails
from briton.backend.briton_request import model_input_to_briton_request
from briton.backend.default_backend import DefaultBackend
from briton.backend.utils import collect_text
from briton.data_structures import or_true
from briton.error_handling import grpc_error_handling
from briton.openai import remove_suffix_from_text
from briton.proto import InferenceAnswerPart
from briton.schema import ModelInput


class LegacyBackend(DefaultBackend):
    def __init__(self):
        super().__init__()

    # Overrides parent
    async def accepts_request(self, model_input: ModelInput) -> Optional[RequestDetails]:
        if self._config is None or self._tokenizer is None:
            return None

        if self._config.is_openai_compatible:
            return None

        input_ids = model_input.input_ids(self._tokenizer)
        return RequestDetails(input_ids=input_ids)

    async def infer(
        self,
        model_input: ModelInput,
        is_cancelled: Callable[[], Awaitable[bool]],  # TODO(pankaj) Wire up request cancellation
        add_schema_to_cache: Callable[[Dict[str, Any]], Awaitable[str]],
        resolve_lora: Optional[Callable[[str], Optional[int]]],
        request_details: RequestDetails,
    ) -> Union[AsyncGenerator[str, None], str]:
        if (
            self._config is None
            or self._tokenizer is None
            or self._briton_stub is None
            or self._generate_request_id is None
        ):
            raise ValueError("Model is not loaded.")
        input_ids = request_details.input_ids
        if input_ids is None:
            raise ValueError("Input ids are None.")

        request_id = self._generate_request_id()
        briton_request = await model_input_to_briton_request(
            request_id=request_id,
            model_input=model_input,
            input_ids=input_ids,
            tokenizer_eos_token_id=self._tokenizer.eos_token_id,
            tokenizer_pad_token_id=self._tokenizer.pad_token_id,
            add_schema_to_cache=add_schema_to_cache,
            resolve_lora=resolve_lora,
            default_max_tokens=self._config.default_max_tokens,
            max_seq_len=self._config.max_seq_len,
        )

        resp_iter = self._briton_stub.Infer(briton_request)

        return await self._plaintext_response(
            resp_iter=resp_iter,
            streaming=or_true(model_input.stream),
            eos_token=self._tokenizer.eos_token,
            tool_call_token=self._config.tool_call_token,
            stop_words=model_input.stop,
            skip_special_tokens=model_input.skip_special_tokens,
        )

    @staticmethod
    async def _plaintext_response(
        resp_iter: AsyncGenerator[InferenceAnswerPart, None],
        streaming: bool,
        eos_token: str,
        tool_call_token: Optional[str],
        stop_words: Optional[List[str]],
        skip_special_tokens: Optional[List[str]],
    ) -> Union[AsyncGenerator[str, None], str]:
        with grpc_error_handling():
            if streaming:
                # Advance the iterator to get the first chunk, to allow any
                # validation error to be thrown. Any errors will be handled
                # gy grpc_error_handling and converted to HTTPException.
                # `first_chunk` is not discarded, it is used below.
                async for first_chunk in resp_iter:
                    break

                async def generate_processed_after_first_chunk():
                    output_text = first_chunk.output_text
                    # Try to remove tool call token from first chunk only
                    if tool_call_token is not None:
                        output_text = output_text.removeprefix(tool_call_token)
                    yield remove_suffix_from_text(
                        text=output_text,
                        eos_token=eos_token,
                        stop_words=stop_words,
                        skip_special_tokens=skip_special_tokens,
                    )

                    async for chunk in resp_iter:
                        output_text = chunk.output_text
                        yield remove_suffix_from_text(
                            text=output_text,
                            eos_token=eos_token,
                            stop_words=stop_words,
                            skip_special_tokens=skip_special_tokens,
                        )

                return generate_processed_after_first_chunk()
            else:
                full_text, _ = await collect_text(resp_iter, eos_token)
                full_text = remove_suffix_from_text(
                    text=full_text,
                    eos_token=eos_token,
                    stop_words=stop_words,
                    skip_special_tokens=skip_special_tokens,
                )
                if tool_call_token is not None:
                    full_text = full_text.removeprefix(tool_call_token)
                return full_text
