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
