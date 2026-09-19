---
description: Streamlit interface standards for the technical-documentation RAG chatbot.
globs: ["**/*.py", "**/streamlit*", "**/.streamlit/**/*"]
alwaysApply: true
---

# Streamlit Interface Standards

## User Experience

The primary interface is a focused technical Q&A workspace. Prioritize a clear question-to-answer flow over dashboard decoration:

- Show the application name, indexed source status, and current limitations.
- Provide a readable chat history with distinct user and assistant messages.
- Display citations or expandable source excerpts for every grounded answer.
- Show loading, empty-index, no-results, provider-error, and partial-ingestion states explicitly.
- Provide a clear reset conversation action and preserve conversation state only for the active session unless persistence is specified.
- Offer document ingestion or re-indexing controls only when the user is authorized to use them.
- Keep technical terminology, file names, and code blocks legible on desktop and mobile widths.

## Streamlit Patterns

- Keep `st.session_state` orchestration in the UI layer; do not hide business state inside global module variables.
- Cache immutable or expensive resources such as model clients, embedding clients, and vector-store connections with the appropriate Streamlit cache primitive.
- Cache data only when invalidation is explicit and tied to source/index changes.
- Avoid rebuilding embeddings or reloading every file on every rerun.
- Keep widgets stable by assigning explicit keys and separating configuration controls from chat rendering.
- Disable submit controls during in-flight work when duplicate requests would be harmful.
- Handle exceptions at the UI boundary and show safe, actionable messages; log the detailed exception through the configured logger.
- Keep rendering functions small and test pure formatting/source-mapping helpers separately.

## Accessibility and Content

- Use descriptive labels for inputs and buttons; do not rely on placeholder text alone.
- Maintain sufficient contrast and avoid color-only status indicators.
- Render Markdown and code safely through Streamlit's supported APIs; never interpret model output as executable HTML or code.
- Do not expose hidden prompts, credentials, raw embeddings, or internal stack traces.
- Preserve source links, page numbers, and headings when displaying citations.

## UI Tests

Test pure presentation helpers and use a small number of browser or Streamlit integration tests for submitting a question with citations, empty-index behavior, ingestion feedback, conversation reset, and safe rendering of hostile document content.