import httpx

from app.providers.base import LLMProviderError, LLMResult


class OpenRouterProvider:
    """Adaptador HTTPX hacia la API de OpenRouter (chat completions)."""

    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str,
        timeout: float = 30.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        # Permite inyectar un MockTransport en pruebas sin consumo externo
        self.transport = transport

    async def generate(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.3,
        top_p: float = 1.0,
        max_tokens: int = 300,
    ) -> LLMResult:
        if not self.api_key:
            raise LLMProviderError("No se configuró OPENROUTER_API_KEY")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
            "stream": False,
        }

        try:
            async with httpx.AsyncClient(
                timeout=self.timeout, transport=self.transport
            ) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()

        except httpx.TimeoutException as exc:
            raise LLMProviderError("Tiempo de espera agotado") from exc

        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            raise LLMProviderError(f"OpenRouter respondió HTTP {status}") from exc

        except (httpx.RequestError, ValueError) as exc:
            raise LLMProviderError("Error de comunicación con el proveedor") from exc

        try:
            choice = data["choices"][0]
            content = choice["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMProviderError("Formato de respuesta LLM inválido") from exc

        if not isinstance(content, str) or not content.strip():
            # Los modelos de razonamiento pueden gastar todo max_tokens antes de escribir la respuesta
            if choice.get("finish_reason") == "length":
                raise LLMProviderError(
                    "El modelo agotó max_tokens sin generar respuesta; aumenta max_tokens"
                )
            raise LLMProviderError("El modelo devolvió una respuesta vacía")

        return LLMResult(content=content, model=data.get("model") or self.model)
