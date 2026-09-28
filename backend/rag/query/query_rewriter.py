class QueryRewriter:

    def rewrite(
        self,
        query: str,
        conversation_context: str | None = None
    ) -> str:

        query = query.strip()

        if not query:
            raise ValueError("Query cannot be empty.")

        if conversation_context:
            return (
                f"{conversation_context.strip()}\n"
                f"Current question: {query}"
            )

        return query