"""Provider-specific LangChain client construction."""

from __future__ import annotations

from typing import Any

from .config import ConfigurationError, Settings


def create_runtime(settings: Settings) -> tuple[Any, Any]:
    try:
        embeddings = _create_embeddings(settings)
        model = _create_chat_model(settings)
        return embeddings, model
    except ConfigurationError:
        raise
    except Exception as error:
        raise ConfigurationError(
            "The configured provider is unavailable; check its credentials and settings"
        ) from error


def _create_embeddings(settings: Settings) -> Any:
    if settings.embedding_provider == "ollama":
        try:
            from langchain_ollama import OllamaEmbeddings
        except ImportError as error:
            raise ConfigurationError("The Ollama LangChain integration is not installed") from error
        return OllamaEmbeddings(model=settings.embedding_model)
    if settings.embedding_provider == "huggingface":
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
        except ImportError as error:
            raise ConfigurationError("The local embedding integration is not installed") from error
        return HuggingFaceEmbeddings(
            model_name=settings.embedding_model,
            model_kwargs={"local_files_only": True},
            encode_kwargs={"normalize_embeddings": True},
        )
    if settings.embedding_provider == "openai":
        try:
            from langchain_openai import OpenAIEmbeddings
        except ImportError as error:
            raise ConfigurationError("The OpenAI LangChain integration is not installed") from error
        return OpenAIEmbeddings(model=settings.embedding_model)
    raise ConfigurationError("EMBEDDING_PROVIDER must be huggingface or openai")


def _create_chat_model(settings: Settings) -> Any:
    if settings.chat_provider == "ollama":
        try:
            from langchain_ollama import ChatOllama
        except ImportError as error:
            raise ConfigurationError("The Ollama LangChain integration is not installed") from error
        return ChatOllama(model=settings.chat_model, temperature=0)
    if settings.chat_provider == "openai":
        try:
            from langchain_openai import ChatOpenAI
        except ImportError as error:
            raise ConfigurationError("The OpenAI LangChain integration is not installed") from error
        return ChatOpenAI(model=settings.chat_model, temperature=0)
    raise ConfigurationError("CHAT_PROVIDER must be ollama or openai")
