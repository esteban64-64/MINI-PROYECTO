from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import get_settings

class InfoResponse(BaseModel):
    name: str
    version: str
    environment: str
    llm_enabled: bool
    model: str

router = APIRouter(prefix="/api/v1/info", tags=["info"])

@router.get("", response_model=InfoResponse)
async def info() -> InfoResponse:
    settings = get_settings()
    return InfoResponse(
        name="AI Knowledge Assistant",
        version="0.2.0",
        environment="development",
        llm_enabled=bool(settings.openrouter_api_key),
        model=settings.openrouter_model,
    )
