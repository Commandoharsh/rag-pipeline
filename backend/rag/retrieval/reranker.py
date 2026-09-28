from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        results,
        top_k: int = 5
    ):

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if not results:
            return []

        pairs = [
            [query, result.content]
            for result in results
        ]

        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(results, scores),
            key=lambda x: float(x[1]),
            reverse=True
        )

        reranked_results = []

        for result, score in ranked[:top_k]:

            result.score = float(score)

            reranked_results.append(result)

        return reranked_results