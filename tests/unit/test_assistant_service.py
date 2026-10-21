import pytest

from app.services.assistant_service import SYSTEM_PROMPT, AssistantService
from tests.fakes import FakeLLMProvider


@pytest.mark.asyncio
async def test_service_builds_system_and_user_messages():
    provider = FakeLLMProvider()
    service = AssistantService(provider)

    result = await service.ask("¿Qué es un LLM?", temperature=0.5, top_p=0.9, max_tokens=100)

    assert result.content == "Respuesta simulada"
    call = provider.calls[0]
    assert call["messages"] == [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "¿Qué es un LLM?"},
    ]
    assert (call["temperature"], call["top_p"], call["max_tokens"]) == (0.5, 0.9, 100)
