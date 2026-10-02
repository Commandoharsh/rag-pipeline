from backend.rag.generation.answer_generator import AnswerGenerator
from backend.rag.generation.mock_llm import MockLLM


def test_answer_generator():

    generator = AnswerGenerator(
        llm=MockLLM()
    )

    answer = generator.generate(
        question="What is RAG?",
        context="RAG combines information retrieval with generation."
    )

    assert answer
    assert isinstance(answer, str)


def test_empty_context():

    generator = AnswerGenerator(
        llm=MockLLM()
    )

    answer = generator.generate(
        question="What is RAG?",
        context=""
    )

    assert "not find enough information" in answer