from backend.rag.chunking.chunk import Chunk
from backend.rag.retrieval.vector_store import VectorStore


def test_vector_store(tmp_path):

    storage_path = str(tmp_path / "qdrant")

    vector_store = VectorStore(
        collection_name="test_collection",
        vector_size=3,
        storage_path=storage_path
    )

    chunks = [
        Chunk(
            content="Machine learning is useful.",
            metadata={
                "source": "test.pdf",
                "page": "1",
                "chunk_index": "0"
            }
        ),
        Chunk(
            content="Deep learning uses neural networks.",
            metadata={
                "source": "test.pdf",
                "page": "2",
                "chunk_index": "0"
            }
        )
    ]

    embeddings = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0]
    ]

    vector_store.add_chunks(
        chunks,
        embeddings
    )

    results = vector_store.search(
        [1.0, 0.0, 0.0],
        limit=2
    )

    assert len(results) > 0

    stored_chunks = vector_store.get_all_chunks()

    assert len(stored_chunks) == 2

    vector_store.close()