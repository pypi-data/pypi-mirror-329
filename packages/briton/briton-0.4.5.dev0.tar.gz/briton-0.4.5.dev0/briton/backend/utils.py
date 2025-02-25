from briton.proto import FinishReason


async def collect_text(async_text_iter, eos_token: str) -> tuple[str, int]:
    full_text = ""
    num_completion_tokens = 0
    async for delta in async_text_iter:
        num_completion_tokens += len(delta.output_ids)
        full_text += delta.output_text
    # HACK(@bdubayah): To avoid refactoring, just add the eos token if the finish reason should be "stop"
    if delta.finish_reason == FinishReason.END_ID or delta.finish_reason == FinishReason.STOP_WORDS:
        full_text += eos_token
    return full_text, num_completion_tokens
