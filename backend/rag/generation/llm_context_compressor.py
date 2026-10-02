from backend.rag.generation.llm_provider import LLMProvider


class LLMContextCompressor:

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    def compress(
        self,
        query: str,
        content: str,
    ) -> str:

        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        if not content.strip():
            return ""

        prompt = f"""
Extract only the information from the context that is
relevant to answering the question.

Question:
{query}

Context:
{content}

Rules:
- Preserve factual information.
- Remove irrelevant information.
- Do not introduce new facts.
- Do not answer the question.
- Return only the relevant context.
"""

        compressed = self.llm.generate(
            prompt=prompt
        ).strip()

        return compressed or content