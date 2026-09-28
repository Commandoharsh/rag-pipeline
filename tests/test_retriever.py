from backend.rag.chunking.chunk import Chunk
from backend.rag.embeddings.embedding_model import EmbeddingModel
from backend.rag.retrieval.vector_store import VectorStore
from backend.rag.retrieval.retriever import SemanticRetriever


def test_semantic_retriever():

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

    embeddings = embedding_model.encode(
        [chunk.content for chunk in chunks]
    )

    vector_store = VectorStore()

    vector_store.add_chunks(
        chunks,
        embeddings
    )

    retriever = SemanticRetriever(
        embedding_model=embedding_model,
        vector_store=vector_store
    )

    results = retriever.retrieve(
        "How is AI used in medicine?",
        top_k=2
    )

    assert len(results) == 2

    result = results[0]

    assert result.content
    assert result.chunk_id
    assert isinstance(result.score, float)
    assert result.metadata
    assert "source" in result.metadata
    assert "page" in result.metadata


def test_retrieval_result_format():

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
        )
    ]

    embedding_model = EmbeddingModel()

    embeddings = embedding_model.encode(
        [chunk.content for chunk in chunks]
    )

    vector_store = VectorStore()

    vector_store.add_chunks(
        chunks,
        embeddings
    )

    retriever = SemanticRetriever(
        embedding_model=embedding_model,
        vector_store=vector_store
    )

    results = retriever.retrieve(
        "machine learning healthcare",
        top_k=2
    )

    result = results[0]

    assert result.chunk_id
    assert result.content
    assert isinstance(result.score, float)
    assert result.metadata
    assert "source" in result.metadata
    assert "page" in result.metadata