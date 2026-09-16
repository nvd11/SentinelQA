from typing import Optional
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from ..configs.settings import get_settings
from ..utils.logger import logger


def get_llm_model(model_name: Optional[str] = None) -> BaseChatModel:
    """Instantiate and return a LangChain ChatModel instance based on available credentials."""
    settings = get_settings()
    target_model = model_name or settings.DEFAULT_LLM_MODEL

    # Option 1: LiteLLM or OpenAI-compatible custom gateway
    if settings.LITELLM_API_BASE and settings.LITELLM_API_KEY:
        logger.info(f"Initializing ChatOpenAI via LiteLLM gateway: {settings.LITELLM_API_BASE}")
        return ChatOpenAI(
            model=target_model,
            api_key=settings.LITELLM_API_KEY,
            base_url=settings.LITELLM_API_BASE,
            temperature=0.2
        )

    # Option 2: Native Google Gemini
    if settings.GEMINI_API_KEY:
        logger.info(f"Initializing ChatGoogleGenerativeAI with model: {target_model}")
        return ChatGoogleGenerativeAI(
            model=target_model,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.2
        )

    # Option 3: Standard OpenAI
    if settings.OPENAI_API_KEY:
        logger.info(f"Initializing ChatOpenAI with model: {target_model}")
        return ChatOpenAI(
            model=target_model,
            api_key=settings.OPENAI_API_KEY,
            temperature=0.2
        )

    logger.warning("No explicit LLM credentials provided; initializing fallback mock-ready ChatOpenAI")
    return ChatOpenAI(
        model="gpt-4o-mini",
        api_key="mock-key",
        temperature=0.2
    )
