from backend.evaluation.answer_metrics import token_set


def faithfulness_score(
    answer: str,
    context: str
) -> float:

    answer_tokens = token_set(answer)
    context_tokens = token_set(context)

    if not answer_tokens:
        return 0.0

    supported = answer_tokens.intersection(
        context_tokens
    )

    return len(supported) / len(answer_tokens)