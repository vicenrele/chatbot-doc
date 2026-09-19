"""Build the local FAISS snapshot from the configured documents directory."""

from __future__ import annotations

from rag_chatbot.config import Settings
from rag_chatbot.providers import create_runtime
from rag_chatbot.service import build_index


def main() -> None:
    settings = Settings.from_env()
    embeddings, _ = create_runtime(settings)
    result = build_index(settings, embeddings)
    print(f"Indexed {result.manifest.chunk_count} chunks")
    for file_result in result.files:
        print(f"{file_result.status}: {file_result.path} ({file_result.message})")


if __name__ == "__main__":
    main()
