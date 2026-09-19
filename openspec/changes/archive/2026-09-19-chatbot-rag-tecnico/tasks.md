# Tasks

## 1. Application foundation

- [x] 1.1 Create the Python application module layout for configuration, domain models, ingestion, retrieval, generation, Streamlit UI, and tests; verify imports resolve under Python 3.11+.
- [x] 1.2 Add configurable settings for document path, index path, model providers, embedding model, retrieval k/threshold, and file limits; verify invalid or missing settings produce actionable validation errors.
- [x] 1.3 Add the required LangChain, Streamlit, FAISS, PDF, validation, and test dependencies; verify a clean environment installs them successfully.

## 2. Document ingestion

- [x] 2.1 Implement safe Markdown and PDF file validation with extension, size, readability, empty-content, count, and path-traversal checks; verify supported, unsupported, malformed, oversized, and empty fixtures.
- [x] 2.2 Implement Markdown and PDF loading with normalization that preserves headings, code blocks, lists, tables where available, and PDF page metadata; verify metadata on representative fixtures.
- [x] 2.3 Implement structure-aware and recursive chunking with deterministic source and chunk metadata; verify stable chunk IDs, section/page preservation, and configured size/overlap behavior.
- [x] 2.4 Implement corpus hashing and per-file ingestion results for indexed, skipped, and failed files; verify unchanged input produces the same corpus identity and safe partial-failure reporting.

## 3. FAISS index lifecycle

- [x] 3.1 Define the vector-store adapter and typed document/chunk/index models; verify domain tests do not require a live model provider.
- [x] 3.2 Build and persist `index.faiss`, `chunks.json`, and `index_manifest.json` as one validated snapshot; verify counts, deterministic IDs, embedding dimensions, and manifest fields agree.
- [x] 3.3 Load an existing snapshot only when corpus hash, embedding identity, dimensions, distance strategy, and ingestion version are compatible; verify incompatible snapshots are rejected with a rebuild instruction.
- [x] 3.4 Add an explicit full rebuild command or service operation with safe trusted-local persistence and progress/results reporting; verify repeated rebuilds do not duplicate chunks.

## 4. Retrieval and grounded generation

- [x] 4.1 Implement configurable FAISS retrieval with top-k, score threshold, bounded context, and typed evidence results; verify relevant, irrelevant, empty-index, and mixed-source queries.
- [x] 4.2 Implement grounded prompt construction that treats retrieved text as untrusted evidence, requires citations, and refuses unsupported answers; verify prompt-injection, insufficient-context, and citation scenarios with fake models.
- [x] 4.3 Implement typed handling for retrieval failure, model failure, timeout, missing configuration, and unsupported questions; verify safe error categories and redacted logs.

## 5. Streamlit interface

- [x] 5.1 Implement the Streamlit chat workspace with active-session history, index status, question submission, loading state, reset action, and empty-index behavior; verify pure rendering helpers independently.
- [x] 5.2 Cache compatible model, embedding, and index resources without rebuilding on normal reruns; verify cache identity changes when the index manifest changes.
- [x] 5.3 Render grounded answers with readable expandable citations and safe Markdown/code output; verify source mapping, mobile-readable content, and hostile document text are handled safely.
- [x] 5.4 Add authorized ingestion/rebuild controls and safe user-facing provider errors; verify unauthenticated or unauthorized flows cannot trigger administrative indexing actions.

## 6. Verification and documentation

- [x] 6.1 Add unit and integration tests covering validation, metadata, chunking, deterministic indexing, manifest compatibility, retrieval, grounding, citations, and UI states; verify the default suite runs without credentials.
- [x] 6.2 Add opt-in provider-backed tests and mark them so they never run in the default suite; verify missing credentials skip or fail with an explicit actionable message.
- [x] 6.3 Document setup, environment variables, supported formats, rebuild workflow, generated index artifacts, security boundaries, and local commands; verify a new developer can run the documented setup and Streamlit command.
- [x] 6.4 Run `pytest -q`, `ruff check .`, `ruff format --check .`, and `mypy .`; verify the focused and full checks pass before considering the capability complete.