from backend.evaluation.rag_evaluator import RAGEvaluator


def test_rag_evaluator():

    evaluator = RAGEvaluator()

    metrics = evaluator.evaluate(
        question="What is RAG?",
        answer="RAG combines retrieval with generation.",
        reference_answer="RAG combines retrieval with generation.",
        context="RAG combines retrieval with generation."
    )

    assert "answer_overlap" in metrics
    assert "faithfulness" in metrics
    assert "answer_relevance" in metrics

    assert 0.0 <= metrics["answer_overlap"] <= 1.0
    assert 0.0 <= metrics["faithfulness"] <= 1.0
    assert 0.0 <= metrics["answer_relevance"] <= 1.0