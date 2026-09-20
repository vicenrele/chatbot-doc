"""Streamlit entry point for the technical documentation chatbot."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings

from rag_chatbot.config import ConfigurationError, Settings
from rag_chatbot.domain import IndexManifest, RetrievedSource
from rag_chatbot.generation import Answer, GenerationError, generate_answer
from rag_chatbot.index import IndexCompatibilityError, SnapshotStore
from rag_chatbot.ingestion import save_uploaded_files
from rag_chatbot.providers import create_runtime
from rag_chatbot.retrieval import RetrievalError, RetrievalSettings, retrieve
from rag_chatbot.service import build_index, ensure_index


def main() -> None:
    st.set_page_config(page_title="Technical Documentation Chatbot", page_icon="📚")
    st.title("Technical Documentation Chatbot")
    try:
        settings = Settings.from_env()
    except ConfigurationError as error:
        st.error(f"Configuration error: {error}")
        return

    st.sidebar.caption(f"Documents: {settings.documents_path}")
    st.sidebar.caption(f"Index: {settings.index_path}")
    if settings.admin_ingestion_enabled:
        uploaded_files = st.sidebar.file_uploader(
            "Add Markdown or PDF files",
            type=["md", "markdown", "pdf"],
            accept_multiple_files=True,
            help="Files are saved locally and added to the next index rebuild.",
        )
        if st.sidebar.button("Add files and rebuild index"):
            _add_files_and_rebuild(settings, uploaded_files)
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if st.sidebar.button("Reset conversation"):
        st.session_state.messages = []
        st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            for source in message.get("sources", []):
                st.caption(source)

    question = st.chat_input("Ask about the documentation")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("Generating answer..."):
                answer = _answer_question(settings, question)
            st.markdown(answer.content)
            for source in answer.sources:
                st.caption(_source_label(source))
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer.content,
                "sources": [_source_label(source) for source in answer.sources],
            }
        )


def _answer_question(settings: Settings, question: str) -> Answer:
    if len(question) > settings.max_question_length:
        return Answer("The question exceeds the configured length limit.", (), False)
    if not (settings.index_path / "index_manifest.json").is_file():
        return Answer(
            "No compatible document index is available. Build the index first.", (), False
        )
    try:
        embeddings, model = _load_runtime(settings)
        index_result = ensure_index(settings, embeddings)
        store = _load_index(str(settings.index_path), index_result.manifest, embeddings)
        sources = retrieve(
            store,
            question,
            RetrievalSettings(
                settings.retrieval_k,
                settings.retrieval_score_threshold,
                settings.max_context_characters,
            ),
        )
        return generate_answer(model, question, sources)
    except (IndexCompatibilityError, RetrievalError, GenerationError, ConfigurationError) as error:
        return Answer(f"The request could not be completed: {error}", (), False)
    except (FileNotFoundError, OSError, ValueError):
        return Answer(
            "The document index could not be prepared. Check the documents and model configuration.",
            (),
            False,
        )


def _add_files_and_rebuild(settings: Settings, uploaded_files: list[Any]) -> None:
    if not uploaded_files:
        st.sidebar.warning("Select at least one Markdown or PDF file first.")
        return
    try:
        file_results = save_uploaded_files(uploaded_files, settings)
        failed_files = [result for result in file_results if result.status == "failed"]
        for result in file_results:
            if result.status == "saved":
                st.sidebar.success(f"Added {result.path}")
            else:
                st.sidebar.error(f"Skipped {result.path}: {result.message}")
        if failed_files:
            return
        embeddings, _ = _load_runtime(settings)
        build_result = build_index(settings, embeddings)
        st.sidebar.success(f"Index rebuilt with {build_result.manifest.chunk_count} chunks")
        _load_runtime.clear()
        _load_index.clear()
    except (ConfigurationError, OSError, ValueError):
        st.sidebar.error("The files could not be added or the index could not be rebuilt")


@st.cache_resource
def _load_runtime(settings: Settings) -> tuple[Any, Any]:
    return create_runtime(settings)


@st.cache_resource
def _load_index(index_path: str, expected_manifest: IndexManifest, embeddings: Embeddings) -> FAISS:
    return SnapshotStore(Path(index_path)).load(embeddings, expected_manifest)


def _source_label(source: RetrievedSource) -> str:
    label = source.filename
    if source.section:
        label += f" - {source.section}"
    if source.page:
        label += f" (p. {source.page})"
    return label


if __name__ == "__main__":
    main()
