from backend.rag.retrieval.retrieval_result import RetrievalResult
from backend.rag.generation.context_builder import ContextBuilder


def test_context_builder():

    results = [
        RetrievalResult(
            chunk_id="paper.pdf_5_2",
            content="RAG combines retrieval with generation.",
            score=0.92,
            metadata={
                "source": "paper.pdf",
                "page": "5"
            }
        )
    ]

    builder = ContextBuilder()

    context = builder.build(results)

    assert "RAG combines retrieval with generation." in context
    assert "paper.pdf" in context
    assert "Page: 5" in context
    assert "paper.pdf_5_2" in context