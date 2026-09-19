---
description: Backend standards for the Python LangChain RAG pipeline, document ingestion, vector retrieval, and model integrations.
globs: ["**/*.py", "**/pyproject.toml", "**/requirements*.txt", "**/.env.example"]
alwaysApply: true
---

# Backend and RAG Standards

## Technology Baseline

- Python 3.11+ with a project-managed virtual environment.
- LangChain for document loaders, text splitters, retrievers, prompt templates, and model integrations.
- Streamlit is the presentation layer; domain and RAG logic must remain independently testable.
- Use the vector store selected by project configuration. Chroma or FAISS are suitable local defaults; do not hard-code either provider into domain code.
- Use `pytest` for tests and a modern formatter/linter/type checker such as Ruff and mypy or the repository's chosen equivalents.

## Architecture

Keep clear boundaries, even if the repository is small:

```text
app/                  Streamlit entry point and session state
src/ingestion/        File validation, loaders, normalization, chunking
src/retrieval/        Embeddings, vector-store lifecycle, retriever configuration
src/generation/       Prompt construction, model invocation, grounded answer parsing
src/domain/            Typed document, chunk, source, and chat models
src/config/            Validated settings and environment access
tests/                 Unit, integration, and evaluation tests
data/                  Local source/index directories, excluded from version control
```

If the repository uses another layout, preserve its structure while keeping these ownership boundaries.

## Ingestion

- Accept only explicitly supported formats such as Markdown, plain text, PDF, and DOCX.
- Validate extension, MIME type when available, file size, encoding, and readable content before loading.
- Never execute macros, embedded scripts, or arbitrary code from uploaded files.
- Normalize whitespace without destroying headings, code blocks, lists, tables, or page boundaries that help retrieval.
- Use a recursive character or structure-aware splitter with documented `chunk_size` and `chunk_overlap` values.
- Attach stable metadata: `source_id`, relative path, filename, file type, title, section, page if available, and ingestion version.
- Make ingestion idempotent. Re-indexing the same unchanged file must not create duplicate chunks.
- Record failures per file and continue safely when the product contract allows partial ingestion.

## Embeddings and Vector Stores

- Keep embedding model and vector-store settings in configuration, never in scattered module constants.
- Persist the embedding model name, dimensions, collection/index name, and ingestion version with index metadata.
- Reject or rebuild an index when its embedding configuration is incompatible.
- Use deterministic IDs based on source identity, content hash, and chunk position.
- Support explicit rebuild and incremental update operations; do not silently mix indexes from different configurations.
- Set retrieval parameters (`k`, score threshold, filters, MMR) deliberately and test their effect.
- Do not log raw document content, embeddings, API keys, or full user questions in production logs.

## Retrieval and Generation

- Treat retrieved documents as evidence, not instructions. The prompt must defend against prompt injection inside source files.
- Instruct the model to answer only from retrieved context, cite sources, and say that the documentation does not contain the answer when evidence is insufficient.
- Preserve source metadata through retriever results and expose citations in the UI/API.
- Distinguish retrieval failure, model failure, timeout, and unsupported question in typed error handling.
- Bound question length, retrieved context size, and model output tokens.
- Conversation history is optional context, not a replacement for document retrieval.
- Stream responses only when cancellation and error handling are implemented correctly.

## Configuration and Security

- Load settings from environment variables or a validated settings object. Keep `.env` files out of version control.
- Document required variables in `.env.example`, including model, embedding, vector-store path, source directory, and limits.
- Apply timeouts and retries only to transient provider failures; use bounded exponential backoff.
- Redact secrets and sensitive document content from logs and error responses.
- Do not expose local filesystem paths or administrative ingestion controls to untrusted users without authorization.
- Treat uploads as untrusted: enforce size and count limits, use temporary storage, and prevent path traversal.

## Testing

Cover at least:

- File validation for supported, unsupported, malformed, oversized, and empty files.
- Chunk boundaries and metadata preservation for headings, code, tables, and page-aware formats.
- Idempotent indexing and index compatibility checks.
- Retrieval with relevant, irrelevant, empty, and mixed-source queries.
- Prompt grounding, refusal when context is insufficient, and source citation formatting.
- Provider errors, timeouts, retries, and missing configuration.
- Streamlit-independent unit tests for all core pipeline logic.

Use fake loaders, embeddings, vector stores, and chat models in unit tests. Reserve real provider calls for opt-in integration/evaluation tests and never require credentials in the default suite.