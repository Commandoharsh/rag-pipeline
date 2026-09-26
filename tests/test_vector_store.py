from backend.rag.chunking.chunk import Chunk
from backend.rag.embeddings.embedding_model import EmbeddingModel
from backend.rag.retrieval.vector_store import VectorStore


def test_vector_store():

    chunks = [
        Chunk(
            content="Machine learning is used in healthcare.",
            metadata={
                "source": "healthcare.pdf",
                "page": "1",
                "chunk_index": "0"
            }
        ),
        Chunk(
            content="The solar system contains planets and stars.",
            metadata={
                "source": "astronomy.pdf",
                "page": "2",
                "chunk_index": "0"
            }
        ),
        Chunk(
            content="Deep learning models use neural networks.",
            metadata={
                "source": "ai.pdf",
                "page": "3",
                "chunk_index": "0"
            }
        )
    ]

    embedding_model = EmbeddingModel()

    texts = [
        chunk.content
        for chunk in chunks
    ]

    embeddings = embedding_model.encode(texts)

    store = VectorStore()

    store.add_chunks(
        chunks,
        embeddings
    )

    query = "How is AI used in medicine?"

    query_embedding = embedding_model.encode_single(
        query
    )

    results = store.search(
        query_embedding,
        limit=2
    )

    assert len(results) == 2

    assert results[0].payload["content"]

    assert "metadata" in results[0].payload