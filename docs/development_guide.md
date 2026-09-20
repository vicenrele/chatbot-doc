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
python -m pip install -e ".[dev]"
```

For local chat, install Ollama separately, start its service, and pull the configured model:

```powershell
ollama serve
ollama pull llama3.2
```

Create `.env` from `.env.example`. Never commit the resulting file. Typical settings include:

```env
CHAT_PROVIDER=ollama
CHAT_MODEL=llama3.2
EMBEDDING_PROVIDER=huggingface
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
VECTOR_STORE_PATH=./data/vector_store
DOCUMENTS_PATH=./data/documents
RETRIEVAL_K=4
```

The local configuration does not require `OPENAI_API_KEY`. To use OpenAI instead, set both provider variables to `openai`, choose compatible model names, and set `OPENAI_API_KEY`. The first run downloads the local embedding model and may take additional time and disk space.

## Run the Application

```bash
streamlit run app.py
```

Open the URL printed by Streamlit. The app should report whether the source directory and compatible vector index are available.

## Ingest Documents

The ingestion command or UI action must validate supported file types and limits, load and normalize documents, split them into chunks with metadata, create or update the vector index, and report indexed, skipped, and failed files. The query path also checks the persisted embedding manifest and automatically rebuilds the FAISS snapshot when the configured embedding space changes. To rebuild manually, run `python scripts/build_index.py` after changing provider or model settings.

## Verification

```bash
pytest -q
ruff check .
ruff format --check .
mypy .
```

Run provider-backed tests only through an explicit integration marker and never require credentials for the default test suite. Manually verify grounded answers with citations, honest insufficient-context responses, safe Markdown/code rendering, useful file-validation errors, and idempotent re-indexing.