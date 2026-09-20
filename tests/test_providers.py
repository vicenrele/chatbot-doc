import pytest

from rag_chatbot.config import ConfigurationError, Settings
from rag_chatbot.providers import create_runtime


def test_provider_configuration_errors_are_safe(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    settings = Settings(
        chat_model="manual-test-chat",
        embedding_model="manual-test-embedding",
        chat_provider="openai",
        embedding_provider="openai",
    )
    with pytest.raises(ConfigurationError, match="provider is unavailable"):
        create_runtime(settings)


def test_local_providers_are_created_without_openai_key(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeEmbeddings:
        def __init__(self, model: str) -> None:
            self.model = model

    class FakeChat:
        def __init__(self, model: str, temperature: int, num_predict: int) -> None:
            self.model = model
            self.temperature = temperature
            self.num_predict = num_predict

    import langchain_ollama

    monkeypatch.setattr(langchain_ollama, "OllamaEmbeddings", FakeEmbeddings)
    monkeypatch.setattr(langchain_ollama, "ChatOllama", FakeChat)
    settings = Settings(
        chat_model="llama3.2",
        embedding_model="nomic-embed-text",
        chat_provider="ollama",
        embedding_provider="ollama",
    )

    embeddings, model = create_runtime(settings)

    assert embeddings.model == "nomic-embed-text"
    assert model.model == "llama3.2"
    assert model.num_predict == 512


def test_openai_providers_remain_explicitly_supported(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeEmbeddings:
        def __init__(self, model: str) -> None:
            self.model = model

    class FakeChat:
        def __init__(self, model: str, temperature: int) -> None:
            self.model = model
            self.temperature = temperature

    import langchain_openai

    monkeypatch.setattr(langchain_openai, "OpenAIEmbeddings", FakeEmbeddings)
    monkeypatch.setattr(langchain_openai, "ChatOpenAI", FakeChat)
    settings = Settings(
        chat_model="gpt-4o-mini",
        embedding_model="text-embedding-3-small",
        chat_provider="openai",
        embedding_provider="openai",
    )

    embeddings, model = create_runtime(settings)

    assert embeddings.model == "text-embedding-3-small"
    assert model.model == "gpt-4o-mini"
