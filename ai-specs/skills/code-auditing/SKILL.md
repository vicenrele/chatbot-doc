---
name: code-auditing
description: Use when auditing the Python LangChain RAG pipeline, Streamlit interface, dependencies, retrieval quality, security, or technical debt.
---

# Code Auditing

Use this skill for focused or comprehensive audits of the technical-documentation chatbot. Read the relevant files under `docs/` before evaluating architecture or behavior.

## Audit Phases

1. Identify Python entry points, package configuration, Streamlit pages, ingestion modules, retrievers, vector-store adapters, prompts, and tests.
2. Run the repository's configured formatter, linter, type checker, and tests as a baseline.
3. Trace one complete path from source file to chunk, embedding, retrieval result, prompt, answer, and citation.
4. Review security: upload validation, path traversal, secrets, prompt injection, unsafe rendering, sensitive logs, and provider permissions.
5. Review quality: deterministic IDs, idempotent indexing, metadata preservation, empty/irrelevant queries, error boundaries, retries, and timeouts.
6. Review Streamlit reruns, cache invalidation, session isolation, duplicate submissions, and accessible states.
7. Report findings by severity with file references, evidence, impact, and a minimal fix.

## RAG-Specific Checks

- Answers must be grounded in retrieved context and include source citations.
- The system must abstain when the corpus does not support an answer.
- Retrieved document text is untrusted data, not executable instructions.
- Embedding model, dimensions, vector-store collection, and ingestion version must be compatible.
- Default tests must run without live model or embedding credentials.
- Retrieval evaluation must distinguish retrieval failure from model-generation failure.

## Output

Return prioritized findings first, then assumptions, test gaps, and a concise summary. Do not report theoretical tool output without verifying it against the code. Recommend established LangChain integrations before custom implementations, accounting for provider lock-in, cost, latency, and testability.