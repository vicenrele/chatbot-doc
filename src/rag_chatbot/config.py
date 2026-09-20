"""Validated application configuration."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


class ConfigurationError(ValueError):
    """Raised when application settings are missing or invalid."""


@dataclass(frozen=True, slots=True)
class Settings:
    documents_path: Path = Path("data/documents")
    index_path: Path = Path("data/vector_store")
    chat_model: str = "llama3.2"
    embedding_model: str = "nomic-embed-text"
    embedding_provider: str = "ollama"
    chat_provider: str = "ollama"
    retrieval_k: int = 4
    retrieval_score_threshold: float = 0.4
    max_file_size_bytes: int = 10_000_000
    max_file_count: int = 100
    max_question_length: int = 2_000
    max_context_characters: int = 24_000
    ingestion_version: str = "1"
    admin_ingestion_enabled: bool = False

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> Settings:
        if environ is None:
            load_dotenv()
        values = os.environ if environ is None else environ
        settings = cls(
            documents_path=Path(values.get("DOCUMENTS_PATH", "data/documents")),
            index_path=Path(values.get("VECTOR_STORE_PATH", "data/vector_store")),
            chat_model=values.get("CHAT_MODEL", "llama3.2"),
            embedding_model=values.get("EMBEDDING_MODEL", "nomic-embed-text"),
            embedding_provider=values.get("EMBEDDING_PROVIDER", "ollama"),
            chat_provider=values.get("CHAT_PROVIDER", "ollama"),
            retrieval_k=_integer(values, "RETRIEVAL_K", 4),
            retrieval_score_threshold=_float(values, "RETRIEVAL_SCORE_THRESHOLD", 0.7),
            max_file_size_bytes=_integer(values, "MAX_FILE_SIZE_BYTES", 10_000_000),
            max_file_count=_integer(values, "MAX_FILE_COUNT", 100),
            max_question_length=_integer(values, "MAX_QUESTION_LENGTH", 2_000),
            max_context_characters=_integer(values, "MAX_CONTEXT_CHARACTERS", 24_000),
            ingestion_version=values.get("INGESTION_VERSION", "1"),
            admin_ingestion_enabled=values.get("ADMIN_INGESTION_ENABLED", "false").lower()
            == "true",
        )
        settings.validate()
        return settings

    def validate(self) -> None:
        if self.retrieval_k < 1:
            raise ConfigurationError("RETRIEVAL_K must be at least 1")
        if not 0 <= self.retrieval_score_threshold <= 1:
            raise ConfigurationError("RETRIEVAL_SCORE_THRESHOLD must be between 0 and 1")
        if self.max_file_size_bytes < 1 or self.max_file_count < 1:
            raise ConfigurationError("File limits must be positive")
        if self.max_question_length < 1 or self.max_context_characters < 1:
            raise ConfigurationError("Question and context limits must be positive")
        if not self.embedding_model:
            raise ConfigurationError("EMBEDDING_MODEL is required")
        if not self.chat_model:
            raise ConfigurationError("CHAT_MODEL is required")
        if self.chat_provider not in {"ollama", "openai"}:
            raise ConfigurationError("CHAT_PROVIDER must be ollama or openai")
        if self.embedding_provider not in {"ollama", "huggingface", "openai"}:
            raise ConfigurationError("EMBEDDING_PROVIDER must be ollama, huggingface, or openai")


def _integer(values: Mapping[str, str], name: str, default: int) -> int:
    raw_value = values.get(name)
    if raw_value is None:
        return default
    try:
        return int(raw_value)
    except ValueError as error:
        raise ConfigurationError(f"{name} must be an integer") from error


def _float(values: Mapping[str, str], name: str, default: float) -> float:
    raw_value = values.get(name)
    if raw_value is None:
        return default
    try:
        return float(raw_value)
    except ValueError as error:
        raise ConfigurationError(f"{name} must be a number") from error
