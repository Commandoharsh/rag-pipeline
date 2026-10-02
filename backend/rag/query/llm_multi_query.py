from backend.rag.generation.llm_provider import LLMProvider


class LLMMultiQueryGenerator:

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    def generate(
        self,
        query: str,
        num_queries: int = 3,
    ) -> list[str]:

        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        prompt = f"""
Generate {num_queries} different search queries
for retrieving documents relevant to the question below.

Original question:
{query}

Rules:
- Preserve the original intent.
- Use different wording for each query.
- Include important technical terminology.
- Do not answer the question.
- Return exactly one query per line.
"""

        response = self.llm.generate(
            prompt=prompt
        )

        queries = []

        for line in response.splitlines():
            line = line.strip()

            if not line:
                continue

            line = line.lstrip(
                "0123456789.-) "
            )

            if line:
                queries.append(line)

        queries.insert(0, query)

        unique_queries = []

        for item in queries:
            if item not in unique_queries:
                unique_queries.append(item)

        return unique_queries[:num_queries + 1]