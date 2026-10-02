from backend.evaluation.answer_metrics import token_set


def answer_relevance_score(
    question: str,
    answer: str
) -> float:

    question_tokens = token_set(question)
    answer_tokens = token_set(answer)

    if not question_tokens:
        return 0.0

    overlap = question_tokens.intersection(
        answer_tokens
    )

    return len(overlap) / len(question_tokens)