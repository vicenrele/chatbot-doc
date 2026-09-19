---
name: show-spec-working
description: Use when the user asks to show, demo, or walk through a RAG chatbot feature, Streamlit workflow, ingestion flow, retrieval result, or documented OpenSpec behavior.
---

# Demonstrate the Chatbot

Demonstrate the requested behavior using the real application and current documentation. Do not stop at a requirements summary.

## Resolve Scope

Identify the active change or feature and list the concrete scenarios to demonstrate. Prefer a local deterministic corpus and fake providers when live credentials are unavailable.

## Streamlit Demonstration

When the feature affects the UI:

1. Start the configured Streamlit app if it is not running.
2. Confirm the source/index readiness state.
3. Submit a question whose answer exists in the corpus.
4. Verify the answer is grounded and displays citations or source excerpts.
5. Submit an unsupported question and verify the insufficient-context response.
6. Check loading, error, reset, and safe Markdown/code rendering states when relevant.

## Pipeline Demonstration

When the feature affects ingestion or retrieval:

1. Use a non-sensitive fixture file.
2. Run ingestion and record indexed, skipped, and failed counts.
3. Query a known fact and inspect retrieved metadata and citations.
4. Re-run ingestion to verify idempotency when applicable.
5. Remove temporary fixtures and restore the local index state.

## Completion

Report the feature demonstrated, commands or UI actions executed, evidence for each scenario, provider/credential limitations, and cleanup status. Never expose secrets or raw sensitive documents.