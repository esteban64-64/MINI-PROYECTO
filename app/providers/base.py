from dataclasses import dataclass
from typing import Protocol


class LLMProviderError(Exception):
    """Error controlado de cualquier proveedor LLM (timeout, HTTP, formato)."""


@dataclass(frozen=True)
class LLMResult:
    content: str
    model: str  # modelo efectivamente servido, si el proveedor lo informa


class LLMProvider(Protocol):
    """Contrato que el servicio usa sin depender de OpenRouter."""

    async def generate(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.3,
        top_p: float = 1.0,
        max_tokens: int = 300,
    ) -> LLMResult: ...
