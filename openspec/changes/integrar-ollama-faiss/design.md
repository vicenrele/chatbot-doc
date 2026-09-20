# Design

## Context

The current runtime constructs only `ChatOpenAI` and `OpenAIEmbeddings`. The FAISS snapshot already stores provider, model, dimensions, distance strategy, corpus identity, and ingestion version in its manifest, but `SnapshotStore.load` currently rejects any mismatch and the Streamlit layer surfaces that rejection as an error. See `proposal.md` for motivation and the delta spec for observable behavior.

## Goals / Non-Goals

**Goals:**

- Keep provider selection behind the existing runtime factory and preserve independent chat and embedding configuration.
- Use Ollama for local chat inference and a local Hugging Face-compatible embedding implementation so the application can run without an OpenAI key.
- Make embedding incompatibility a recoverable index lifecycle event: remove the old snapshot, rebuild from the current corpus, then load only the new compatible snapshot.
- Preserve manifest-based compatibility checks, atomic snapshot replacement, grounded generation, and the existing OpenAI option.
- Make missing Ollama, model, or local embedding prerequisites visible through safe actionable errors.

**Non-Goals:**

- Changing the RAG prompt, retrieval ranking semantics, document formats, or citation contract.
- Shipping model weights or an Ollama server inside the Python package.
- Supporting automatic migration of vectors between embedding spaces; all vectors must be regenerated.
- Adding a hosted free provider or changing deployment infrastructure.

## Decisions

- **Use LangChain provider adapters:** add `langchain-ollama` for the chat client and a local Hugging Face embedding adapter backed by `sentence-transformers`. This matches the current LangChain abstraction and keeps the domain code independent of provider classes. Direct HTTP calls to Ollama were rejected because they would duplicate adapter behavior and error handling.
- **Keep provider settings explicit:** extend validated settings with provider-specific model configuration while retaining `CHAT_PROVIDER`, `CHAT_MODEL`, `EMBEDDING_PROVIDER`, and `EMBEDDING_MODEL`. OpenAI remains opt-in; local mode must not read or require an API key. A local embedding model identity includes its configured model name and dimensions in the manifest.
- **Rebuild at the service/lifecycle boundary:** add a compatibility decision before retrieval and before explicit rebuild operations. If the current manifest cannot be trusted for the requested embedding configuration, delete the application-owned snapshot and call the existing build path. `SnapshotStore.build` remains the atomic writer, so a failed rebuild cannot replace a previously valid snapshot with a partial directory.
- **Treat any embedding-space change as incompatible:** provider, model, dimensions, distance strategy, and relevant embedding configuration are compared exactly. Reusing vectors after only a model-name or provider change is rejected even when dimensions happen to match.
- **Make startup behavior explicit in the UI:** when an index is missing or rebuilt automatically, show a safe status/error message and avoid answering until a compatible snapshot exists. This avoids silently serving stale vectors while keeping provider exceptions out of the UI.
- **Test at two boundaries:** unit-test provider construction with mocked adapter imports and index compatibility with temporary snapshot paths; add an integration-style service test proving a changed embedding manifest triggers deletion and rebuild without requiring a live Ollama server.

## Risks / Trade-offs

- **[Risk]** Local embedding models may require a first-run download and significant disk/RAM. **Mitigation**: document the model download/runtime prerequisite, expose model configuration, and keep OpenAI available as an explicit alternative.
- **[Risk]** Automatic rebuilding can delay the first request after configuration changes. **Mitigation**: perform the rebuild before retrieval, report progress/status in Streamlit, and keep writes atomic.
- **[Risk]** A failed rebuild leaves no usable snapshot if the incompatible snapshot was deleted first. **Mitigation**: retain the existing snapshot until the new build has completed in a separate temporary location where feasible; if deletion is required by the contract, surface the rebuild failure and never load the old incompatible vectors.
- **[Risk]** Different local embedding implementations may report dimensions only after model loading. **Mitigation**: use the existing dimension probe during manifest creation and fail with a safe configuration error before writing a snapshot.

## Migration Plan

1. Add optional local-provider dependencies and update `.env.example`, README, and development guidance with Ollama installation, model-pull, and local embedding setup.
2. Deploy the provider configuration with local chat and embedding model identities.
3. On the first run, treat the existing OpenAI-generated index as incompatible, remove or replace it through the normal rebuild path, and generate a new local index from the corpus.
4. Verify a grounded question and citation output, then retain the old provider settings as the rollback configuration.
5. Roll back by restoring OpenAI provider settings and rebuilding the index again; never reuse vectors generated by the other embedding configuration.

## Open Questions

- The exact default Ollama chat model and local embedding model should be selected during implementation based on the target machine's available memory and acceptable download size; the provider contract and rebuild behavior do not depend on those specific model names.
