import uvicorn
from .configs.settings import get_settings


def main():
    settings = get_settings()
    uvicorn.run(
        "backend.src.server:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=(settings.APP_ENV == "development")
    )


if __name__ == "__main__":
    main()
