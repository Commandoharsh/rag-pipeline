from backend.rag.generation.llm_provider import LLMProvider


class LLMQueryRewriter:

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    def rewrite(
        self,
        query: str,
        conversation_context: str | None = None,
    ) -> str:

        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        context = conversation_context or "None"

        prompt = f"""
Rewrite the following research question into a precise
search query for a retrieval system.

Conversation context:
{context}

Question:
{query}

Rules:
- Preserve the original intent.
- Remove unnecessary conversational wording.
- Keep important technical terminology.
- Do not answer the question.
- Return only the rewritten query.
"""

        rewritten = self.llm.generate(
            prompt=prompt
        ).strip()

        if not rewritten:
            return query

        return rewritten