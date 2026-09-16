from fastapi import APIRouter
from ..configs.settings import get_settings

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    settings = get_settings()
    return {
        "status": "healthy",
        "app": "SentinelQA",
        "version": "0.1.0",
        "environment": settings.APP_ENV
    }
