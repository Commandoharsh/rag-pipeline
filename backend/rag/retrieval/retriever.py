from backend.rag.embeddings.embedding_model import EmbeddingModel
from backend.rag.retrieval.vector_store import VectorStore
from backend.rag.retrieval.retrieval_result import RetrievalResult


class SemanticRetriever:

    def __init__(
        self,
        embedding_model=None,
        vector_store=None
    ):
        self.embedding_model = embedding_model or EmbeddingModel()
        self.vector_store = vector_store or VectorStore()

    def retrieve(self, query: str, top_k: int = 5):

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        query_embedding = self.embedding_model.encode_single(query)

        results = self.vector_store.search(
            query_embedding,
            limit=top_k
        )

        formatted_results = []

        for result in results:

            payload = result.payload

            metadata = payload.get("metadata", {})

            chunk_id = (
                f"{metadata.get('source', 'unknown')}_"
                f"{metadata.get('page', 'unknown')}_"
                f"{metadata.get('chunk_index', '0')}"
            )

            formatted_results.append(
                RetrievalResult(
                    chunk_id=chunk_id,
                    content=payload["content"],
                    score=float(result.score),
                    metadata=metadata
                )
            )

        return formatted_results