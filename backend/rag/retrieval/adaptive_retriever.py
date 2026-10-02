from backend.rag.query.query_intent import QueryIntent


class AdaptiveRetriever:

    def __init__(self, retriever):
        self.retriever = retriever

    def retrieve(
        self,
        query: str,
        intent: QueryIntent,
    ):

        if intent == QueryIntent.COMPARISON:
            retrieval_k = 30
            final_k = 8

        elif intent == QueryIntent.ANALYTICAL:
            retrieval_k = 25
            final_k = 7

        elif intent == QueryIntent.EXPLANATION:
            retrieval_k = 20
            final_k = 5

        elif intent == QueryIntent.DEFINITION:
            retrieval_k = 15
            final_k = 4

        else:
            retrieval_k = 20
            final_k = 5

        return self.retriever.retrieve(
            query,
            retrieval_k=retrieval_k,
            final_k=final_k,
        )