from backend.rag.retrieval.retrieval_result import RetrievalResult
from backend.rag.generation.context_orderer import ContextOrderer


def test_context_ordering():

    results = [
        RetrievalResult("A", "Chunk A", 0.4, {}),
        RetrievalResult("B", "Chunk B", 0.9, {}),
        RetrievalResult("C", "Chunk C", 0.7, {}),
    ]

    orderer = ContextOrderer()

    ordered = orderer.order(results)

    assert ordered[0].chunk_id == "B"
    assert ordered[1].chunk_id == "C"
    assert ordered[2].chunk_id == "A"