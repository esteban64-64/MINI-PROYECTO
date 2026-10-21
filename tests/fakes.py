from app.providers.base import LLMProviderError, LLMResult


class FakeLLMProvider:
    """Proveedor falso: registra llamadas y no consume red."""

    def __init__(self, content: str = "Respuesta simulada", error: str | None = None):
        self.content = content
        self.error = error
        self.calls: list[dict] = []

    async def generate(self, messages, temperature=0.3, top_p=1.0, max_tokens=300):
        self.calls.append(
            {
                "messages": messages,
                "temperature": temperature,
                "top_p": top_p,
                "max_tokens": max_tokens,
            }
        )
        if self.error:
            raise LLMProviderError(self.error)
        return LLMResult(content=self.content, model="fake/model")
