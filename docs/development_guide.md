# Development Guide

## Prerequisites

- Python 3.11 or newer
- `venv`, `uv`, Poetry, or the repository's chosen environment manager
- API credentials only for the selected model and embedding providers
- Optional local vector-store dependencies required by the implementation

## Local Setup

```bash
python -m venv .venv
# Windows PowerShell
.\\.venv\\Scripts\\Activate.ps1
# macOS/Linux
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create `.env` from `.env.example`. Never commit the resulting file. Typical settings include:

```env
CHAT_MODEL=<configured-chat-model>
EMBEDDING_MODEL=<configured-embedding-model>
VECTOR_STORE_PATH=./data/vector_store
DOCUMENTS_PATH=./data/documents
RETRIEVAL_K=4
```

Use the provider-specific API key variable required by the configured LangChain integration.

## Run the Application

```bash
streamlit run app.py
```

Open the URL printed by Streamlit. The app should report whether the source directory and compatible vector index are available.

## Ingest Documents

The ingestion command or UI action must validate supported file types and limits, load and normalize documents, split them into chunks with metadata, create or update the vector index, and report indexed, skipped, and failed files. The exact command is implementation-specific and must be documented in the project README when introduced.

## Verification

```bash
pytest -q
ruff check .
ruff format --check .
mypy .
```

Run provider-backed tests only through an explicit integration marker and never require credentials for the default test suite. Manually verify grounded answers with citations, honest insufficient-context responses, safe Markdown/code rendering, useful file-validation errors, and idempotent re-indexing.