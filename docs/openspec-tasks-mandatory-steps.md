---
description: Enforce verification steps for OpenSpec tasks in the LangChain RAG and Streamlit project.
alwaysApply: true
---

# OpenSpec Task Verification

When creating or updating an OpenSpec `tasks.md`, read `openspec/config.yaml` first when it exists. If OpenSpec is not initialized, do not invent configuration values; use the project documents under `docs/` as the source of truth.

## Required Task Structure

1. Put branch/setup work first when the repository workflow requires it.
2. Include focused unit tests for the affected ingestion, chunking, retrieval, generation, or UI behavior.
3. Run targeted tests and the configured quality checks.
4. Run integration or evaluation checks when the change crosses a model, embedding, vector-store, or Streamlit boundary.
5. Update technical documentation affected by the change.

## RAG Verification Requirements

For ingestion/indexing changes, verify supported and unsupported files, malformed or empty content, metadata preservation, stable IDs, idempotent re-indexing, and index compatibility.

For retrieval/generation changes, verify relevant questions, irrelevant questions, empty indexes, insufficient context, source citations, prompt-injection text inside documents, provider errors, and bounded input/output behavior.

For Streamlit changes, verify chat submission, reruns, duplicate-submit prevention, loading/error/empty states, conversation reset, citation rendering, and safe Markdown/code display.

Live provider tests must be opt-in, use non-sensitive fixtures, and document required credentials. The default suite must use fakes or deterministic local implementations.

## Completion Evidence

Before marking a task complete, record commands executed, test counts and limitations, provider/browser checks and credential requirements, updated documentation, and remaining retrieval or corpus-freshness risks.

Do not require database snapshots, endpoint `curl` calls, or browser automation for a task that does not expose that boundary. Add those checks only when the implemented application actually has a database, HTTP service, or browser workflow affected by the change.