# Tasks

## 1. Provider Configuration and Dependencies

- [x] 1.1 Add the Ollama and local embedding integration dependencies, verify the editable project installation completes, and preserve OpenAI dependencies for explicit OpenAI mode.
- [x] 1.2 Extend validated settings and `.env.example` with independent provider/model options and local defaults, verify local configuration validates without `OPENAI_API_KEY`.
- [x] 1.3 Implement provider-factory branches for Ollama chat and local Hugging Face embeddings with safe configuration errors, verify unit tests cover local, OpenAI, and unavailable-provider paths.

## 2. Embedding Compatibility and Automatic Rebuild

- [x] 2.1 Define the effective embedding compatibility identity used by the manifest, including provider, model, dimensions, distance strategy, corpus identity, and ingestion version, and verify manifest round-trip tests preserve it.
- [x] 2.2 Add a lifecycle operation that detects an incompatible or incomplete snapshot, removes or replaces it safely, and rebuilds from the current corpus before retrieval, verifying unchanged manifests reuse the snapshot.
- [x] 2.3 Verify changed provider/model/dimension settings trigger a full FAISS rebuild and never load stale vectors, using temporary index paths and fake embeddings without live providers.
- [x] 2.4 Verify failed automatic rebuilds leave no partial snapshot available for retrieval and return a safe actionable error.

## 3. Application Integration and Documentation

- [x] 3.1 Integrate compatibility detection and automatic rebuild into startup, explicit rebuild, and Streamlit query paths, verifying the UI reports rebuild/provider failures without secrets or stack traces.
- [x] 3.2 Update README and development guidance with Ollama installation, model download, local embedding prerequisites, configuration examples, and OpenAI rollback instructions, verifying the documented commands match the project configuration.
- [x] 3.3 Add or update focused tests for provider selection, automatic rebuild, grounded answers, and OpenAI compatibility, then verify `pytest -q` passes.
- [x] 3.4 Run `ruff check .`, `ruff format --check .`, and `mypy .`, resolving only issues introduced by this change.
