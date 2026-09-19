# Technical Documentation Chatbot

This repository contains the agent configuration and technical standards for a technical-documentation chatbot built with LangChain and Streamlit. The target application uses retrieval-augmented generation (RAG), vector databases, and local or uploaded files as its knowledge source.

## Product Scope

The assistant should:

- Ingest supported Markdown, text, PDF, and DOCX documentation.
- Split content into retrievable chunks while preserving useful metadata.
- Store embeddings in a configurable vector store.
- Retrieve relevant evidence for each question.
- Answer from the retrieved documentation, cite its sources, and abstain when evidence is insufficient.
- Provide a focused Streamlit chat interface with ingestion/index status and safe rendering.

This repository is configuration and documentation, not the application implementation. The application can use these standards as its initial architecture and should update them as concrete dependencies and modules are selected.

## Local Application

The initial implementation is a local-first Streamlit RAG application using FAISS for a mostly static documentation corpus.

```powershell
$python = "$env:LocalAppData\Programs\Python\Python312\python.exe"
& $python -m pip install -e ".[dev]"
Copy-Item .env.example .env
& $python scripts/build_index.py
streamlit run app.py
```

Set `OPENAI_API_KEY`, `EMBEDDING_MODEL`, and `CHAT_MODEL` in `.env`. The first implementation supports OpenAI through LangChain's provider adapter; model and embedding identities are recorded in the FAISS manifest.

To add files from the Streamlit sidebar, set `ADMIN_INGESTION_ENABLED=true`, select one or more Markdown/PDF files, and click **Add files and rebuild index**. The files are copied into `data/documents/` and become queryable after the rebuild completes. The control stays disabled by default.

Place Markdown or PDF files under `data/documents/`. A rebuild creates the application-owned snapshot under `data/vector_store/`:

- `index.faiss`: vector index.
- `index.pkl`: LangChain's trusted local document-store metadata.
- `chunks.json`: deterministic chunk text and citation metadata.
- `index_manifest.json`: corpus and embedding compatibility metadata.

Only load snapshots generated in this directory. Do not place user-uploaded serialized files there. Set `ADMIN_INGESTION_ENABLED=true` to expose the rebuild control in Streamlit; leave it disabled for read-only chat deployments.

Run the checks with:

```powershell
& $python -m pytest -q
& $python -m ruff check .
& $python -m ruff format --check .
& $python -m mypy .
```

## Configuration Map

- `AGENTS.md`, `CLAUDE.md`, `codex.md`, and `GEMINI.md`: entry points for agent-specific tooling.
- `docs/base-standards.md`: cross-cutting rules and project context.
- `docs/backend-standards.md`: Python/LangChain ingestion, retrieval, generation, security, and testing.
- `docs/frontend-standards.md`: Streamlit UI, session state, caching, accessibility, and UI tests.
- `docs/data-model.md`: logical document, chunk, index, citation, and conversation model.
- `docs/api-spec.yml`: optional HTTP contract for a split service deployment.
- `docs/development_guide.md`: local environment and verification commands.
- `ai-specs/agents/`: role guidance for backend, frontend, and product analysis.
- `ai-specs/skills/`: reusable workflow guidance; keep the canonical source here.

## Recommended Architecture

```text
source files -> validation/loaders -> normalization/chunking
             -> embeddings/vector store -> retriever
             -> grounded prompt/model -> answer + citations -> Streamlit
```

Keep provider-specific code behind adapters and keep the RAG pipeline testable without live API credentials.

## Working with the Configuration

1. Read `docs/base-standards.md` and the relevant specialist standard.
2. Inspect the real application repository before assuming paths, dependencies, or providers.
3. Implement one pipeline boundary at a time: ingestion, indexing, retrieval, generation, or UI.
4. Add focused tests with fake model and vector-store integrations.
5. Update the affected documentation and run the checks in `docs/development_guide.md`.

## OpenSpec

When OpenSpec is initialized in the application repository, configure its context to include the documents in this repository and the relevant files under `ai-specs/`. Keep the product context above as the source of truth for stack, data flow, and quality expectations.