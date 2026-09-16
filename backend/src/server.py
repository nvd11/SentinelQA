from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .configs.settings import get_settings
from .routers import health_router, scan_router
from .utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger.info(f"Starting SentinelQA API Server in [{settings.APP_ENV}] mode...")
    yield
    logger.info("Shutting down SentinelQA API Server...")


def create_app() -> FastAPI:
    app = FastAPI(
        title="SentinelQA (AutoTestAgent) API",
        description="Autonomous QA Agent API for Semantic Coverage & JUnit 5 Self-Healing",
        version="0.1.0",
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(scan_router)

    return app


app = create_app()
