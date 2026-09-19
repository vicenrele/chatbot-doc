"""Application services for building and querying the local index."""

from __future__ import annotations

from dataclasses import dataclass

from langchain_core.embeddings import Embeddings

from .config import Settings
from .domain import FileIngestionResult, IndexManifest
from .index import SnapshotStore, dimension_for, manifest_for
from .ingestion import corpus_hash, ingest_directory


@dataclass(frozen=True, slots=True)
class BuildResult:
    manifest: IndexManifest
    files: tuple[FileIngestionResult, ...]


def build_index(settings: Settings, embeddings: Embeddings) -> BuildResult:
    settings.validate()
    chunks, results = ingest_directory(settings.documents_path, settings)
    manifest = manifest_for(
        corpus_hash(settings.documents_path, settings),
        settings.embedding_provider,
        settings.embedding_model,
        dimension_for(embeddings),
        settings.ingestion_version,
        len(chunks),
    )
    SnapshotStore(settings.index_path).build(chunks, embeddings, manifest)
    return BuildResult(manifest, tuple(results))
