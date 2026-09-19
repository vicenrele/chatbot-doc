---
description: Standards for maintaining the technical documentation chatbot's documentation and agent specifications.
alwaysApply: true
---

# Documentation Standards

- Write technical artifacts in English; preserve source-document language in examples and product requirements when relevant.
- Keep `docs/base-standards.md` as the single source of truth for cross-cutting engineering rules.
- Update `backend-standards.md` when ingestion, retrieval, model, vector-store, security, or dependency behavior changes.
- Update `frontend-standards.md` when Streamlit workflows, state, accessibility, or rendering changes.
- Update `data-model.md` when document, chunk, index, source, or conversation contracts change.
- Update `api-spec.yml` when an HTTP endpoint, schema, status code, or error contract changes.
- Update `development_guide.md` when setup, environment variables, commands, or test requirements change.
- Keep examples executable or clearly label them as pseudocode. Never document credentials or real sensitive content.
- Prefer short sections, stable headings, explicit assumptions, and terminology consistent with the RAG pipeline.
- Before completion, check internal links, YAML front matter, OpenAPI syntax, and consistency between docs and agent roles.