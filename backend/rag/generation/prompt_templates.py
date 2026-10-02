SYSTEM_PROMPT = """
You are ResearchRAG, an AI assistant for research and
technical knowledge.

Answer questions using only the supplied context.

Rules:
1. Do not invent facts.
2. If the context does not contain enough information,
   clearly say that the information is not available.
3. Prefer precise and concise answers.
4. Preserve important technical terminology.
5. Cite the provided sources using their source identifiers.
"""


USER_PROMPT_TEMPLATE = """
Context:

{context}

Question:

{question}

Instructions:

Answer the question using the context above.
When making a factual claim, identify the relevant source.
"""


def build_prompt(
    question: str,
    context: str
) -> str:

    return USER_PROMPT_TEMPLATE.format(
        question=question,
        context=context
    )