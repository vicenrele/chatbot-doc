# RAG Data Model

This document defines the logical model for the technical-documentation chatbot. A physical database is optional for the first local implementation; the model still governs metadata, IDs, and boundaries.

## Document

Represents one indexed source file: `source_id`, relative `path`, `filename`, `file_type`, `content_hash`, `title`, `ingestion_version`, and source update time.

## DocumentChunk

Represents the retrieval unit: `chunk_id`, `source_id`, normalized `text`, `chunk_index`, `section`, optional `page`, and provider-safe metadata. IDs are deterministic from source identity, content hash, and position.

## EmbeddingIndex

Represents the vector-store compatibility contract: `index_id`, provider, exact `embedding_model`, dimensions, distance metric, ingestion version, document count, and lifecycle timestamps. Incompatible embedding configurations require an explicit rebuild.

## RetrievedSource

Represents evidence returned for a question: `chunk_id`, `source_id`, evidence text, similarity `score`, result `rank`, and user-facing citation data such as filename, section, page, or link.

## ChatTurn

Represents one active-session message: `role` (`user` or `assistant`), content, attached sources, timestamp, and correlation `request_id`.

## Relationships

```text
Document 1 ---- * DocumentChunk * ---- 1 EmbeddingIndex
                                      |
                                      *
                                 RetrievedSource

ChatTurn(user) -> retrieval -> RetrievedSource -> ChatTurn(assistant)
```

## Invariants

- Every chunk belongs to exactly one source document.
- Every citation maps to a real chunk in the current index.
- Duplicate ingestion of unchanged content is idempotent.
- An assistant answer without supporting sources must be marked ungrounded or replaced by an insufficient-context response.
- Conversation history must never be treated as authoritative documentation.