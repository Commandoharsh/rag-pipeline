from backend.rag.embeddings.embedding_model import EmbeddingModel


def test_embedding_model():

    model = EmbeddingModel()

    texts = [
        "Artificial intelligence is transforming healthcare.",
        "Machine learning is used for medical diagnosis."
    ]

    embeddings = model.encode(texts)

    assert embeddings.shape[0] == 2

    assert embeddings.shape[1] == 384


def test_single_embedding():

    model = EmbeddingModel()

    embedding = model.encode_single(
        "Retrieval augmented generation"
    )

    assert len(embedding) == 384