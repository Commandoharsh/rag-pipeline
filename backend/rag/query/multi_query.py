class MultiQueryGenerator:

    def generate(
        self,
        query: str,
        num_queries: int = 3
    ) -> list[str]:

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        queries = [
            query,
            f"Explain {query}",
            f"What are the key concepts related to {query}?"
        ]

        return queries[:num_queries]