---
description: Core development rules for the technical documentation chatbot.
alwaysApply: true
---

# Core Project Standards

## Project Context

This project builds a technical-documentation chatbot with Python, LangChain, and Streamlit. It uses retrieval-augmented generation (RAG): source files are loaded, split into meaningful chunks, embedded, indexed in a vector store, retrieved for each question, and passed to a language model with the retrieved context.

The primary workflow is:

1. Ingest supported documentation files.
2. Validate, normalize, and chunk their contents.
3. Create embeddings and persist a vector index.
4. Retrieve relevant chunks for a user question.
5. Generate an answer grounded in those chunks.
6. Display the answer and source references in Streamlit.

## Engineering Principles

- Make small, focused, reversible changes.
- Keep ingestion, retrieval, generation, and presentation as separate responsibilities.
- Prefer typed Python interfaces and explicit data models over unstructured dictionaries.
- Write tests for parsing, chunking, retrieval, prompt construction, and answer-source behavior.
- Never claim facts that are not supported by retrieved context. The assistant must state when the indexed documentation is insufficient.
- Treat source documents as untrusted input: validate file types and sizes, avoid executing file contents, and protect secrets.
- Make external model, embedding, and vector-store providers configurable through environment variables.
- Preserve document metadata such as source path, title, section, page, and chunk identifier throughout the pipeline.
- Keep user-facing errors actionable without exposing credentials, prompts, stack traces, or internal paths.

## Language and Naming

- Code, tests, comments, logs, configuration keys, and technical documentation use English.
- The Streamlit interface may support Spanish or another product language, but UI copy must be intentional and documented.
- Use descriptive `snake_case` names for Python modules, functions, and variables; `PascalCase` for classes; and `UPPER_SNAKE_CASE` for constants.

## Quality Gates

- Add or update focused tests before implementation when behavior changes.
- Run formatting, linting, type checking, and the targeted test suite for the affected slice.
- Run the full test suite before declaring a cross-cutting RAG or UI change complete.
- For retrieval changes, evaluate groundedness, source attribution, empty-index behavior, and irrelevant-question behavior.
- Update documentation whenever dependencies, supported file formats, environment variables, architecture, or contracts change.

## Source Documents

- `docs/backend-standards.md`: ingestion, retrieval, persistence, security, and testing.
- `docs/frontend-standards.md`: Streamlit interface and interaction standards.
- `docs/data-model.md`: document, chunk, embedding, retrieval, and conversation concepts.
- `docs/api-spec.yml`: optional service contract for health and chat endpoints.
- `docs/development_guide.md`: local setup and verification workflow.
- `docs/documentation-standards.md`: documentation maintenance rules.
- `ai-specs/agents/`: role-specific guidance for implementation and analysis.