# Proposal

## Why

The project needs a simple, local-first technical documentation chatbot that can answer questions from a mostly static corpus of Markdown and PDF files. A focused RAG pipeline will provide grounded answers with source citations without introducing a remote vector database or unnecessary operational complexity.

## What Changes

- Add ingestion for validated Markdown and PDF documentation files.
- Normalize and split documents into retrievable chunks while preserving headings, pages, and source metadata.
- Generate embeddings and persist a FAISS index for the corpus.
- Persist chunk metadata and an index manifest alongside the FAISS index.
- Rebuild the index explicitly when the corpus or embedding configuration changes.
- Add retrieval and grounded answer generation through LangChain.
- Add a Streamlit chat interface with index status, citations, empty-index handling, and insufficient-context responses.
- Keep vector-store access behind an adapter so a future migration to ChromaDB does not affect the RAG domain logic.

## Capabilities

### New Capabilities

- `technical-documentation-rag`: Ingest technical documents, build and validate a local FAISS index, retrieve relevant evidence, and present grounded answers with citations through Streamlit.

### Modified Capabilities

<!-- No existing capability requirements are being modified. -->

## Impact

- Adds a Python application layer using Streamlit and LangChain.
- Adds configurable embedding and chat-model integrations.
- Adds FAISS and local persisted index artifacts under an ignored data directory.
- Introduces ingestion, retrieval, generation, configuration, and presentation modules with focused tests.
- Requires documentation for supported files, environment variables, index rebuilds, and local verification.