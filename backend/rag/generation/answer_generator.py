from backend.rag.generation.llm_provider import LLMProvider
from backend.rag.generation.prompt_templates import (
    SYSTEM_PROMPT,
    build_prompt,
)


class AnswerGenerator:

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    def generate(
        self,
        question: str,
        context: str
    ) -> str:

        if not question.strip():
            raise ValueError("Question cannot be empty.")

        if not context.strip():
            return (
                "I could not find enough information "
                "in the provided documents to answer this question."
            )

        prompt = build_prompt(
            question=question,
            context=context
        )

        return self.llm.generate(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT
        )