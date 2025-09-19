from typing import Optional, List
from llama_cpp import Llama


class LlamaRunner:
    """Thin wrapper around llama-cpp-python for text generation."""

    def __init__(self, model_path: str, n_ctx: int = 4096, n_gpu_layers: int = 0, n_threads: Optional[int] = None) -> None:
        self.llm = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_gpu_layers=n_gpu_layers,
            n_threads=n_threads,
            verbose=False,
        )

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.2, top_p: float = 0.9) -> str:
        out = self.llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stop=["</s>", "<|eot_id|>"],
        )
        text = out.get("choices", [{}])[0].get("text", "")
        return text.strip()
