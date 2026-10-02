from backend.rag.chunking.chunk import Chunk
from backend.rag.embeddings.embedding_model import EmbeddingModel
from backend.rag.retrieval.retrieval_result import RetrievalResult
from backend.rag.retrieval.retriever import SemanticRetriever
from backend.rag.retrieval.vector_store import VectorStore


def create_store(tmp_path):

    return VectorStore(
        collection_name="test_collection",
        vector_size=384,
        storage_path=str(
            tmp_path / "qdrant"
        )
    )


def test_semantic_retriever(tmp_path):

    vector_store = create_store(
        tmp_path
    )

    embedding_model = EmbeddingModel()

    chunk = Chunk(
        content=(
            "Artificial intelligence "
            "is transforming healthcare."
        ),
        metadata={
            "source": "test.pdf",
            "page": "1",
            "chunk_index": "0"
        }
    )

    embedding = embedding_model.encode(
        [chunk.content]
    )

    vector_store.add_chunks(
        [chunk],
        embedding
    )

    retriever = SemanticRetriever(
        embedding_model=embedding_model,
        vector_store=vector_store
    )

    results = retriever.retrieve(
        "artificial intelligence healthcare",
        top_k=1
    )

    assert len(results) == 1
    assert isinstance(
        results[0],
        RetrievalResult
    )

    vector_store.close()


def test_retrieval_result_format(tmp_path):

    vector_store = create_store(
        tmp_path
    )

    embedding_model = EmbeddingModel()

    chunk = Chunk(
        content="Machine learning is useful.",
        metadata={
            "source": "test.pdf",
            "page": "1",
            "chunk_index": "0"
        }
    )

    embedding = embedding_model.encode(
        [chunk.content]
    )

    vector_store.add_chunks(
        [chunk],
        embedding
    )

    retriever = SemanticRetriever(
        embedding_model=embedding_model,
        vector_store=vector_store
    )

    results = retriever.retrieve(
        "machine learning",
        top_k=1
    )

    result = results[0]

    assert isinstance(
        result,
        RetrievalResult
    )

    assert isinstance(
        result.chunk_id,
        str
    )

    assert isinstance(
        result.content,
        str
    )

    assert isinstance(
        result.score,
        float
    )

    assert isinstance(
        result.metadata,
        dict
    )

    vector_store.close()