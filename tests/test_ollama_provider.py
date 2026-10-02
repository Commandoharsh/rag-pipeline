import pytest

from backend.rag.generation.ollama_provider import OllamaProvider


def test_ollama_provider_configuration():
    provider = OllamaProvider(
        model="llama3.2",
        base_url="http://localhost:11434"
    )

    assert provider.model == "llama3.2"
    assert provider.base_url == "http://localhost:11434"


def test_ollama_provider_requires_prompt():
    provider = OllamaProvider()

    with pytest.raises(ValueError):
        provider.generate("")