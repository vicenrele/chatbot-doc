"""Evidence retrieval and bounded context preparation."""

from __future__ import annotations

from dataclasses import dataclass

from langchain_community.vectorstores import FAISS

from .domain import RetrievedSource


class RetrievalError(RuntimeError):
    """Raised when retrieval cannot complete safely."""


@dataclass(frozen=True, slots=True)
class RetrievalSettings:
    k: int = 4
    score_threshold: float = 0.4
    max_context_characters: int = 24_000


def retrieve(store: FAISS, question: str, settings: RetrievalSettings) -> list[RetrievedSource]:
    if not question.strip():
        return []
    try:
        results = store.similarity_search_with_score(question, k=settings.k)
    except Exception as error:
        raise RetrievalError("Document retrieval failed") from error
    sources: list[RetrievedSource] = []
    context_size = 0
    for rank, (document, distance) in enumerate(results, start=1):
        score = 1.0 / (1.0 + float(distance))
        if score < settings.score_threshold:
            continue
        metadata = document.metadata
        text = document.page_content
        if context_size + len(text) > settings.max_context_characters:
            break
        sources.append(
            RetrievedSource(
                chunk_id=str(metadata.get("chunk_id", "")),
                source_id=str(metadata.get("source_id", "")),
                evidence=text,
                score=float(score),
                rank=rank,
                filename=str(metadata.get("filename", "unknown")),
                section=metadata.get("section"),
                page=metadata.get("page"),
            )
        )
        context_size += len(text)
    return sources


def format_citation(source: RetrievedSource) -> str:
    location = source.filename
    if source.section:
        location += f" - {source.section}"
    if source.page:
        location += f" (p. {source.page})"
    return f"[{source.rank}] {location}"
