from backend.rag.embeddings.embedding_model import EmbeddingModel
from backend.rag.retrieval.vector_store import VectorStore
from backend.rag.retrieval.bm25_retriever import BM25Retriever


class ApplicationState:

    def __init__(self):

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore(
            collection_name="research_documents",
            vector_size=384,
            storage_path="data/qdrant"
        )

        self.bm25_retriever = BM25Retriever()

        # Rebuild BM25 from persistent Qdrant data.
        indexed_chunks = (
            self.vector_store.get_all_chunks()
        )

        if indexed_chunks:
            self.bm25_retriever.index(
                indexed_chunks
            )

        self.initialized = True

    def close(self):

        self.vector_store.close()