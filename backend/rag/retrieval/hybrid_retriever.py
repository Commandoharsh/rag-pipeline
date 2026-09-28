from backend.rag.retrieval.rrf import reciprocal_rank_fusion


class HybridRetriever:

    def __init__(
        self,
        semantic_retriever,
        bm25_retriever
    ):
        self.semantic_retriever = semantic_retriever
        self.bm25_retriever = bm25_retriever

    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ):

        dense_results = self.semantic_retriever.retrieve(
            query,
            top_k=top_k
        )

        bm25_results = self.bm25_retriever.retrieve(
            query,
            top_k=top_k
        )

        fused_results = reciprocal_rank_fusion(
            [dense_results, bm25_results],
            top_k=top_k
        )

        return fused_results