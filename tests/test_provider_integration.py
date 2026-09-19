import os

import pytest


@pytest.mark.integration
def test_openai_provider_configuration_is_opt_in() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY is required for provider-backed tests")
    pytest.importorskip("langchain_openai")
