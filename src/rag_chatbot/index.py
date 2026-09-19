"""FAISS snapshot lifecycle and vector-store adapter."""

from __future__ import annotations

import json
import shutil
from collections.abc import Sequence
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Protocol

from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings

from .domain import DocumentChunk, IndexManifest


class IndexCompatibilityError(ValueError):
    """Raised when persisted index metadata does not match requested settings."""


class VectorStoreAdapter(Protocol):
    def search(self, query: str, k: int) -> list[tuple[DocumentChunk, float]]: ...


class SnapshotStore:
    """Persist FAISS vectors and application-owned chunk metadata together."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def build(
        self,
        chunks: Sequence[DocumentChunk],
        embeddings: Embeddings,
        manifest: IndexManifest,
    ) -> None:
        if not chunks:
            raise ValueError("Cannot build an index without document chunks")
        temporary_path = self.path.with_name(f"{self.path.name}.tmp")
        if temporary_path.exists():
            shutil.rmtree(temporary_path)
        temporary_path.mkdir(parents=True)
        texts = [chunk.text for chunk in chunks]
        metadata = [
            dict(chunk.metadata, chunk_id=chunk.chunk_id, chunk_index=chunk.chunk_index)
            for chunk in chunks
        ]
        vector_store = FAISS.from_texts(texts, embeddings, metadatas=metadata, normalize_L2=True)
        vector_store.save_local(str(temporary_path), index_name="index")
        _write_json(temporary_path / "chunks.json", [_chunk_to_dict(chunk) for chunk in chunks])
        _write_json(temporary_path / "index_manifest.json", _manifest_to_dict(manifest))
        if self.path.exists():
            shutil.rmtree(self.path)
        temporary_path.rename(self.path)

    def load(self, embeddings: Embeddings, expected: IndexManifest) -> FAISS:
        manifest_path = self.path / "index_manifest.json"
        chunks_path = self.path / "chunks.json"
        if not manifest_path.exists() or not chunks_path.exists():
            raise IndexCompatibilityError("Index snapshot is incomplete; rebuild is required")
        actual = _manifest_from_dict(json.loads(manifest_path.read_text(encoding="utf-8")))
        if actual != expected:
            raise IndexCompatibilityError(
                "Index configuration is incompatible; explicit rebuild is required"
            )
        chunks = json.loads(chunks_path.read_text(encoding="utf-8"))
        if len(chunks) != actual.chunk_count:
            raise IndexCompatibilityError("Index metadata count is invalid; rebuild is required")
        # The directory is application-owned and is never populated from uploads.
        return FAISS.load_local(
            str(self.path), embeddings, index_name="index", allow_dangerous_deserialization=True
        )

    def manifest(self) -> IndexManifest:
        return _manifest_from_dict(
            json.loads((self.path / "index_manifest.json").read_text(encoding="utf-8"))
        )


def manifest_for(
    corpus_hash: str,
    embedding_provider: str,
    embedding_model: str,
    dimensions: int,
    ingestion_version: str,
    chunk_count: int,
) -> IndexManifest:
    return IndexManifest(
        corpus_hash,
        embedding_provider,
        embedding_model,
        dimensions,
        "L2",
        ingestion_version,
        chunk_count,
    )


def dimension_for(embeddings: Embeddings) -> int:
    vector = embeddings.embed_query("dimension probe")
    return len(vector)


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2, default=str), encoding="utf-8")


def _chunk_to_dict(chunk: DocumentChunk) -> dict[str, object]:
    return {
        "chunk_id": chunk.chunk_id,
        "source_id": chunk.source_id,
        "text": chunk.text,
        "chunk_index": chunk.chunk_index,
        "section": chunk.section,
        "page": chunk.page,
        "metadata": chunk.metadata,
    }


def _manifest_to_dict(manifest: IndexManifest) -> dict[str, object]:
    data = asdict(manifest)
    data["created_at"] = manifest.created_at.isoformat()
    return data


def _manifest_from_dict(data: dict[str, object]) -> IndexManifest:
    data = dict(data)
    created_at = data.get("created_at")
    if isinstance(created_at, str):
        data["created_at"] = datetime.fromisoformat(created_at)
    return IndexManifest(**data)  # type: ignore[arg-type]
