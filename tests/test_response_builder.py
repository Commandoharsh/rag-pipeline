from backend.rag.generation.response_builder import ResponseBuilder
from backend.rag.retrieval.retrieval_result import RetrievalResult


def test_response_builder():

    result = RetrievalResult(
        chunk_id="paper.pdf_4_2",
        content="RAG combines retrieval with generation.",
        score=0.91,
        metadata={
            "source": "paper.pdf",
            "page": "4"
        }
    )

    builder = ResponseBuilder()

    response = builder.build(
        answer="RAG combines retrieval and generation [SOURCE 1].",
        results=[result],
        citation_ids=[1]
    )

    assert response.answer
    assert len(response.citations) == 1
    assert response.citations[0].source == "paper.pdf"
    assert response.citations[0].page == "4"