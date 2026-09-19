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