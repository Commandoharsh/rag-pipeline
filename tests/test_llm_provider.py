from backend.rag.generation.mock_llm import MockLLM


def test_mock_llm():

    llm = MockLLM()

    response = llm.generate(
        "What is RAG?"
    )

    assert response
    assert isinstance(response, str)