from typing import Any, AsyncGenerator, Awaitable, Callable, Dict, Optional, Union

from openai.types.chat import ChatCompletion

from briton.backend.backend_types import (
    InferBackend,
    LazyLoadParams,
    LoadParams,
    RequestDetails,
)
from briton.backend.briton_request import (
    model_input_to_briton_request,
    openai_spec_response,
)
from briton.data_structures import or_default, or_false
from briton.openai import generate_tool_call_id, generate_tool_call_id_vllm
from briton.proto import InferenceRequest
from briton.schema import ModelInput


class DefaultBackend(InferBackend):
    """Regular OpenAI spec support backend."""

    def __init__(self):
        self._tokenizer = None
        self._briton_stub = None
        self._generate_request_id = None
        self._config = None

    def load(self, load_params: LoadParams) -> None:
        self._tokenizer = load_params.tokenizer
        self._generate_request_id = load_params.generate_request_id
        self._config = load_params.config

    async def lazy_load(self, lazy_load_params: LazyLoadParams) -> None:
        self._briton_stub = lazy_load_params.briton_stub

    async def accepts_request(self, model_input: ModelInput) -> Optional[RequestDetails]:
        if self._config is None or self._tokenizer is None:
            return None

        if not self._config.is_openai_compatible:
            return None

        input_ids = model_input.input_ids(self._tokenizer)
        return RequestDetails(input_ids=input_ids)

    @staticmethod
    def _tool_call_id_fn(
        use_vllm_tool_call_id_style: Optional[bool],
    ) -> Optional[Callable[[], str]]:
        if or_false(use_vllm_tool_call_id_style):
            return generate_tool_call_id_vllm
        else:
            return generate_tool_call_id

    async def infer(
        self,
        model_input: ModelInput,
        is_cancelled: Callable[[], Awaitable[bool]],  # TODO(pankaj) Wire up request cancellation
        add_schema_to_cache: Callable[[Dict[str, Any]], Awaitable[str]],
        resolve_lora: Optional[Callable[[str], Optional[int]]],
        request_details: RequestDetails,
    ) -> Union[AsyncGenerator[str, None], ChatCompletion]:
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

        # TODO(bdubayah): replace with num_return_sequences in Briton
        # This is a workaround to send n requests, which would be equivalent to
        # sampling n return sequences in the same request
        resp_iters = [self._briton_stub.Infer(briton_request)]
        if model_input.n is not None and model_input.n > 1:
            for i in range(1, model_input.n):
                new_request = InferenceRequest()
                new_request.CopyFrom(briton_request)
                new_request.request_id = self._generate_request_id()
                new_request.random_seed = new_request.random_seed + 1
                resp_iters.append(self._briton_stub.Infer(new_request))

        return await openai_spec_response(
            resp_iters=resp_iters,
            request_id=str(request_id),
            num_input_ids=len(input_ids),
            streaming=or_false(model_input.stream),
            eos_token=self._tokenizer.eos_token,
            tool_call_token=self._config.tool_call_token,
            tool_call_id_fn=self._tool_call_id_fn(self._config.use_vllm_tool_call_id_style),
            model_name=or_default(model_input.model, ""),
            include_stream_usage=model_input.include_stream_usage,
            stop_words=model_input.stop,
            skip_special_tokens=model_input.skip_special_tokens,
            is_chat_completion=model_input._is_chat_completion,
        )
