"""Typed domain models shared by the RAG pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


def utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass(frozen=True, slots=True)
class SourceDocument:
    source_id: str
    relative_path: str
    filename: str
    file_type: str
    content_hash: str
    title: str | None = None
    updated_at: datetime = field(default_factory=utc_now)


@dataclass(frozen=True, slots=True)
class DocumentChunk:
    chunk_id: str
    source_id: str
    text: str
    chunk_index: int
    section: str | None = None
    page: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RetrievedSource:
    chunk_id: str
    source_id: str
    evidence: str
    score: float
    rank: int
    filename: str
    section: str | None = None
    page: int | None = None


@dataclass(frozen=True, slots=True)
class IndexManifest:
    corpus_hash: str
    embedding_provider: str
    embedding_model: str
    dimensions: int
    distance_strategy: str
    ingestion_version: str
    chunk_count: int
    created_at: datetime = field(default_factory=utc_now)

    def compatibility_key(self) -> tuple[object, ...]:
        return (
            self.corpus_hash,
            self.embedding_provider,
            self.embedding_model,
            self.dimensions,
            self.distance_strategy,
            self.ingestion_version,
            self.chunk_count,
        )


@dataclass(frozen=True, slots=True)
class FileIngestionResult:
    path: str
    status: str
    message: str
    chunk_count: int = 0
