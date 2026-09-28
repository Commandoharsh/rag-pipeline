from backend.rag.chunking.chunk import Chunk
from backend.rag.retrieval.bm25_retriever import BM25Retriever


def test_bm25_retriever():

    chunks = [
        Chunk(
            content="BERT is a transformer model used for natural language processing.",
            metadata={
                "source": "nlp.pdf",
                "page": "1",
                "chunk_index": "0"
            }
        ),
        Chunk(
            content="Convolutional neural networks are widely used for image classification.",
            metadata={
                "source": "vision.pdf",
                "page": "2",
                "chunk_index": "0"
            }
        ),
        Chunk(
            content="Reinforcement learning trains agents through rewards.",
            metadata={
                "source": "rl.pdf",
                "page": "3",
                "chunk_index": "0"
            }
        )
    ]

    retriever = BM25Retriever()

    retriever.index(chunks)

    results = retriever.retrieve(
        "BERT transformer",
        top_k=2
    )

    assert len(results) == 2
    assert "BERT" in results[0].content
    assert results[0].chunk_id
    assert isinstance(results[0].score, float)
    assert results[0].metadata


def test_bm25_empty_query():

    chunks = [
        Chunk(
            content="Machine learning is used in healthcare.",
            metadata={
                "source": "healthcare.pdf",
                "page": "1",
                "chunk_index": "0"
            }
        )
    ]

    retriever = BM25Retriever()
    retriever.index(chunks)

    try:
        retriever.retrieve("")
        assert False
    except ValueError:
        assert True


def test_bm25_requires_index():

    retriever = BM25Retriever()

    try:
        retriever.retrieve("machine learning")
        assert False
    except ValueError:
        assert True