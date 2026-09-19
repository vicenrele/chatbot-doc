from pathlib import Path

import pytest

from rag_chatbot.config import ConfigurationError, Settings
from rag_chatbot.ingestion import chunk_documents, corpus_hash, load_document, save_uploaded_files


class FakeUpload:
    def __init__(self, name: str, content: bytes) -> None:
        self.name = name
        self._content = content
        self.size = len(content)

    def getvalue(self) -> bytes:
        return self._content


def test_settings_require_model_names() -> None:
    with pytest.raises(ConfigurationError, match="EMBEDDING_MODEL"):
        Settings.from_env({"CHAT_MODEL": "chat"})


def test_markdown_preserves_title_and_deterministic_chunks(tmp_path: Path) -> None:
    document = tmp_path / "guide.md"
    document.write_text(
        "# Setup\n\nInstall the package.\n\n## Usage\n\nRun the app.", encoding="utf-8"
    )
    settings = Settings(embedding_model="embed", chat_model="chat")
    loaded = load_document(document, tmp_path, settings)
    first = chunk_documents(loaded, settings)
    second = chunk_documents(load_document(document, tmp_path, settings), settings)
    assert loaded[0].source.title == "Setup"
    assert first[0].chunk_id == second[0].chunk_id
    assert first[0].metadata["filename"] == "guide.md"


def test_corpus_hash_changes_with_content(tmp_path: Path) -> None:
    document = tmp_path / "guide.md"
    document.write_text("one", encoding="utf-8")
    settings = Settings(embedding_model="embed", chat_model="chat")
    original = corpus_hash(tmp_path, settings)
    document.write_text("two", encoding="utf-8")
    assert corpus_hash(tmp_path, settings) != original


def test_question_without_index_returns_safe_message(tmp_path: Path) -> None:
    from app import _answer_question

    settings = Settings(
        documents_path=tmp_path / "documents",
        index_path=tmp_path / "missing-index",
        embedding_model="embed",
        chat_model="chat",
    )
    answer = _answer_question(settings, "What is documented?")
    assert "index" in answer.content.lower()
    assert answer.grounded is False


def test_uploaded_files_are_saved_with_safe_validation(tmp_path: Path) -> None:
    settings = Settings(
        documents_path=tmp_path / "documents",
        embedding_model="embed",
        chat_model="chat",
    )
    results = save_uploaded_files([FakeUpload("../guide.md", b"# Guide\n\nUse the app.")], settings)
    assert results[0].status == "saved"
    assert (settings.documents_path / "guide.md").read_text(encoding="utf-8").startswith("# Guide")


def test_uploaded_files_reject_unsupported_and_empty_content(tmp_path: Path) -> None:
    settings = Settings(
        documents_path=tmp_path / "documents",
        embedding_model="embed",
        chat_model="chat",
    )
    results = save_uploaded_files(
        [FakeUpload("secret.txt", b"secret"), FakeUpload("empty.md", b"")], settings
    )
    assert [result.status for result in results] == ["failed", "failed"]
