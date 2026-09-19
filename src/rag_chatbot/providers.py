"""Provider-specific LangChain client construction."""

from __future__ import annotations

from typing import Any

from .config import ConfigurationError, Settings


def create_runtime(settings: Settings) -> tuple[Any, Any]:
    if settings.embedding_provider != "openai" or settings.chat_provider != "openai":
        raise ConfigurationError(
            "Set EMBEDDING_PROVIDER=openai and CHAT_PROVIDER=openai for the configured runtime"
        )
    try:
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    except ImportError as error:
        raise ConfigurationError("The OpenAI LangChain integration is not installed") from error
    try:
        return (
            OpenAIEmbeddings(model=settings.embedding_model),
            ChatOpenAI(model=settings.chat_model, temperature=0),
        )
    except Exception as error:
        raise ConfigurationError(
            "The configured provider is unavailable; check its credentials and settings"
        ) from error
