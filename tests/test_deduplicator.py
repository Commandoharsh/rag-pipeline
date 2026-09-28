from backend.rag.chunking.chunk import Chunk
from backend.rag.retrieval.retrieval_result import RetrievalResult
from backend.rag.retrieval.deduplicator import ResultDeduplicator


def test_deduplication():

    result_a = RetrievalResult(
        chunk_id="A",
        content="First chunk",
        score=0.9,
        metadata={}
    )

    result_a_duplicate = RetrievalResult(
        chunk_id="A",
        content="First chunk",
        score=0.8,
        metadata={}
    )

    result_b = RetrievalResult(
        chunk_id="B",
        content="Second chunk",
        score=0.7,
        metadata={}
    )

    deduplicator = ResultDeduplicator()

    results = deduplicator.deduplicate(
        [result_a, result_a_duplicate, result_b]
    )

    assert len(results) == 2
    assert results[0].chunk_id == "A"
    assert results[1].chunk_id == "B"