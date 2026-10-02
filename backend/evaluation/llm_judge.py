import json
import re


class LLMJudge:

    def __init__(self, llm):
        self.llm = llm

    def evaluate(
        self,
        question: str,
        context: str,
        answer: str,
        reference_answer: str = "",
    ):

        prompt = f"""
You are evaluating a RAG system.

Evaluate the generated answer using the supplied question,
context, and reference answer.

Question:
{question}

Retrieved Context:
{context}

Reference Answer:
{reference_answer}

Generated Answer:
{answer}

Score each category from 1 to 5.

1. Relevance:
Does the answer directly address the question?

2. Faithfulness:
Are the claims supported by the retrieved context?

3. Correctness:
Does the answer agree with the reference answer when
a reference answer is available?

Return ONLY valid JSON:

{{
    "relevance": 1,
    "faithfulness": 1,
    "correctness": 1,
    "reason": "brief explanation"
}}
"""

        raw_response = self.llm.generate(
            prompt=prompt
        )

        return self._parse_response(
            raw_response
        )

    def _parse_response(self, response: str):

        response = response.strip()

        # Remove Markdown JSON fences if the LLM adds them.
        response = re.sub(
            r"^```json\s*",
            "",
            response,
            flags=re.IGNORECASE,
        )

        response = re.sub(
            r"\s*```$",
            "",
            response,
        )

        try:
            data = json.loads(response)

        except json.JSONDecodeError:

            return {
                "relevance": None,
                "faithfulness": None,
                "correctness": None,
                "reason": (
                    "LLM judge returned invalid JSON."
                ),
                "raw_response": response,
            }

        return {
            "relevance": data.get("relevance"),
            "faithfulness": data.get("faithfulness"),
            "correctness": data.get("correctness"),
            "reason": data.get("reason", ""),
        }