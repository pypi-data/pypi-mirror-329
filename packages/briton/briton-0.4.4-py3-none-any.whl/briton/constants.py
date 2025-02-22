# TODO(pankaj) Pick this from truss constants, once a small lib is extracted out of truss.
import string

OPENAI_COMPATIBLE_TAG = "openai-compatible"
DEFAULT_BRITON_PORT = 50051
DEFAULT_TP_COUNT = 1

# Use a directory that can be picked up by baseten-fs, if enabled
FSM_CACHE_DIR = "/cache/model/fsm_cache"

DEFAULT_MAX_FSM_WORKERS = 10

TOOL_CALL_IDS = {
    "llama": 128010,
    "mistral": 5,
    "palmyra": 151657,
    "qwen": 151657,
}

TOOL_CALL_TOKENS = {
    "llama": "<|python_tag|>",
    "mistral": "[TOOL_CALLS]",
    "palmyra": "<tool_call>",
    "qwen": "<tool_call>",
}

# vLLM uses the format `chatcmpl-tool-` followed by a length 32
# alphanumeric string: chatcmpl-tool-ace101101c7149f2b0ef11d5ef6bf694
#
# Note that Llama and its variants don't internally use the tool call id,
# so this id could be anything.
#
# Mistral's chat template expects a length 9 alphanumeric string, so we can't
# use the vLLM tool call id style.
USE_VLLM_TOOL_CALL_ID_STYLE = {
    "llama": True,
    "mistral": False,
    "palmyra": True,
    "qwen": True,
}


MODEL_INPUT_TO_BRITON_FIELD = {
    "max_tokens": "request_output_len",
    "beam_width": "beam_width",
    "repetition_penalty": "repetition_penalty",
    "presence_penalty": "presence_penalty",
    "temperature": "temperature",
    "length_penalty": "len_penalty",
    "end_id": "end_id",
    "pad_id": "pad_id",
    "runtime_top_k": "runtime_top_k",
    "runtime_top_p": "runtime_top_p",
    "random_seed": "random_seed",
    "stop_words": "stop_words",
    "bad_words": "bad_words",
}

# TODO(bdubayah): Don't hardcode this
LOCAL_PREDICT_ENDPOINT = "http://localhost:8080/v1/models/model:predict"

UINT32_MAX = 2**32 - 1

ALPHANUMERIC_CHARS = string.ascii_letters + string.digits

BRITON_DEFAULT_MAX_TOKENS = 50

TRT_CONFIG_FILENAME = "config.json"
