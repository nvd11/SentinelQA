from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_ENV: str = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    # LLM Providers
    LITELLM_API_BASE: Optional[str] = None
    LITELLM_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    DEFAULT_LLM_MODEL: str = "gemini-2.5-pro"

    # LangChain / LangSmith
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: Optional[str] = None
    LANGCHAIN_PROJECT: str = "SentinelQA"

    # Agent Limits
    MAX_HEALING_ITERATIONS: int = 3
    COMMAND_TIMEOUT_SECONDS: int = 180
    SANDBOX_TEMP_DIR: str = "/tmp/sentinelqa/sandboxes"

    # Integrations
    GITHUB_TOKEN: Optional[str] = None
    JIRA_SERVER_URL: Optional[str] = None
    JIRA_USERNAME: Optional[str] = None
    JIRA_API_TOKEN: Optional[str] = None


@lru_cache()
def get_settings() -> Settings:
    return Settings()
