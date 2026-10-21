"""Experimento 5: fallos del proveedor simulados con httpx.MockTransport (sin consumo externo)."""
import httpx
import pytest

from app.providers.base import LLMProviderError
from app.providers.openrouter import OpenRouterProvider

API_KEY = "sk-test-secret"
MESSAGES = [{"role": "user", "content": "hola"}]


def make_provider(handler) -> OpenRouterProvider:
    return OpenRouterProvider(
        api_key=API_KEY,
        model="test/model",
        base_url="https://openrouter.test/api/v1",
        transport=httpx.MockTransport(handler),
    )


@pytest.mark.asyncio
async def test_success_extracts_content_and_sends_payload():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["auth"] = request.headers["Authorization"]
        seen["url"] = str(request.url)
        seen["json"] = request.read()
        return httpx.Response(
            200,
            json={"model": "served/model", "choices": [{"message": {"content": "Hola!"}}]},
        )

    result = await make_provider(handler).generate(MESSAGES, max_tokens=50)

    assert result.content == "Hola!"
    assert result.model == "served/model"
    assert seen["auth"] == f"Bearer {API_KEY}"
    assert seen["url"].endswith("/chat/completions")
    assert b'"max_tokens":50' in seen["json"].replace(b" ", b"")


@pytest.mark.asyncio
async def test_timeout_raises_controlled_error():
    def handler(request):
        raise httpx.ReadTimeout("timeout", request=request)

    with pytest.raises(LLMProviderError, match="Tiempo de espera"):
        await make_provider(handler).generate(MESSAGES)


@pytest.mark.asyncio
async def test_http_429_raises_controlled_error():
    def handler(request):
        return httpx.Response(429, json={"error": "rate limited", "key": API_KEY})

    with pytest.raises(LLMProviderError, match="HTTP 429") as exc_info:
        await make_provider(handler).generate(MESSAGES)
    assert API_KEY not in str(exc_info.value)


@pytest.mark.asyncio
async def test_response_without_choices_raises_controlled_error():
    def handler(request):
        return httpx.Response(200, json={"id": "x"})

    with pytest.raises(LLMProviderError, match="Formato"):
        await make_provider(handler).generate(MESSAGES)


@pytest.mark.asyncio
async def test_empty_content_due_to_token_limit_raises_clear_error():
    def handler(request):
        return httpx.Response(
            200,
            json={"choices": [{"finish_reason": "length", "message": {"content": None}}]},
        )

    with pytest.raises(LLMProviderError, match="agotó max_tokens"):
        await make_provider(handler).generate(MESSAGES)


@pytest.mark.asyncio
async def test_missing_api_key_raises_without_calling_network():
    def handler(request):
        raise AssertionError("No debería llamar a la red")

    provider = make_provider(handler)
    provider.api_key = ""
    with pytest.raises(LLMProviderError, match="OPENROUTER_API_KEY"):
        await provider.generate(MESSAGES)
