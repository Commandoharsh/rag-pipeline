class RerankingPipeline:

    def __init__(
        self,
        retriever,
        reranker
    ):
        self.retriever = retriever
        self.reranker = reranker

    def retrieve(
        self,
        query: str,
        retrieval_k: int = 20,
        final_k: int = 5
    ):

        candidates = self.retriever.retrieve(
            query,
            top_k=retrieval_k
        )

        reranked = self.reranker.rerank(
            query,
            candidates,
            top_k=final_k
        )

        return reranked