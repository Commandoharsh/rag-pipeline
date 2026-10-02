from backend.rag.generation.llm_provider import LLMProvider


class MockLLM(LLMProvider):

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None
    ) -> str:

        return (
            "This is a development response generated from "
            "the provided research context."
        )