from backend.config import settings


def test_settings():
    assert settings.LLM_PROVIDER
    assert settings.OLLAMA_BASE_URL
    assert settings.OLLAMA_MODEL
    assert settings.RAG_TOP_K > 0
    assert settings.RAG_RETRIEVAL_K > 0
    assert settings.RAG_FINAL_K > 0