import pytest
from app.services.assistance_service import BootstrapAssistantService

@pytest.mark.asyncio
async def test_service_responds_to_known_question():
    service = BootstrapAssistantService()
    response = await service.answer("¿Qué es FastAPI?")
    assert "FastAPI" in response.answer
    assert response.provider == "bootstrap-local"

@pytest.mark.asyncio
async def test_service_responds_to_unknown_question():
    service = BootstrapAssistantService()
    response = await service.answer("¿Cómo está el clima?")
    assert "API está operativa" in response.answer
    assert response.provider == "bootstrap-local"