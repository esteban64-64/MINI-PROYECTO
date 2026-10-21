import httpx
import pytest
from httpx import ASGITransport, AsyncClient

from app.api.chat import get_assistant_service
from app.main import app
from app.providers.openrouter import OpenRouterProvider
from app.services.assistant_service import AssistantService
from tests.fakes import FakeLLMProvider

API_KEY = "sk-test-secret"


@pytest.fixture
def fake_provider():
    provider = FakeLLMProvider()
    app.dependency_overrides[get_assistant_service] = lambda: AssistantService(provider)
    yield provider
    app.dependency_overrides.clear()


def override_with_mock_transport(handler):
    provider = OpenRouterProvider(
        api_key=API_KEY,
        model="test/model",
        base_url="https://openrouter.test/api/v1",
        transport=httpx.MockTransport(handler),
    )
    app.dependency_overrides[get_assistant_service] = lambda: AssistantService(provider)


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


async def test_health_endpoint(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


async def test_info_endpoint(client):
    response = await client.get("/api/v1/info")
    assert response.status_code == 200
    assert "llm_enabled" in response.json()


async def test_chat_valid_question(client, fake_provider):
    response = await client.post(
        "/api/v1/chat",
        json={"question": "¿Qué es un LLM?", "temperature": 0.3, "top_p": 1.0, "max_tokens": 300},
    )
    assert response.status_code == 200
    assert response.json() == {"answer": "Respuesta simulada", "model": "fake/model"}
    assert len(fake_provider.calls) == 1


@pytest.mark.parametrize(
    "body",
    [
        {"question": "A"},
        {"question": "Pregunta válida", "temperature": -1},
        {"question": "Pregunta válida", "top_p": 0},
        {"question": "Pregunta válida", "max_tokens": 0},
    ],
)
async def test_chat_invalid_returns_422_without_calling_provider(client, fake_provider, body):
    response = await client.post("/api/v1/chat", json=body)
    assert response.status_code == 422
    assert fake_provider.calls == []


async def test_chat_provider_error_returns_502(client):
    app.dependency_overrides[get_assistant_service] = lambda: AssistantService(
        FakeLLMProvider(error="Tiempo de espera agotado")
    )
    response = await client.post("/api/v1/chat", json={"question": "¿Qué es un LLM?"})
    assert response.status_code == 502


def _timeout(request):
    raise httpx.ReadTimeout("timeout", request=request)


@pytest.mark.parametrize(
    "handler",
    [
        _timeout,
        lambda r: httpx.Response(429, json={"error": "rate limited", "echo": API_KEY}),
        lambda r: httpx.Response(200, json={"id": "sin-choices"}),
    ],
    ids=["timeout", "http_429", "sin_choices"],
)
async def test_provider_failures_return_502_without_leaking_secrets(client, handler):
    override_with_mock_transport(handler)
    response = await client.post("/api/v1/chat", json={"question": "¿Qué es un LLM?"})
    assert response.status_code == 502
    assert API_KEY not in response.text
    assert "rate limited" not in response.text
