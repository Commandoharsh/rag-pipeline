import re


def token_set(text: str) -> set[str]:

    return set(
        re.findall(
            r"\b\w+\b",
            text.lower()
        )
    )


def answer_keyword_overlap(
    answer: str,
    reference: str
) -> float:

    answer_tokens = token_set(answer)
    reference_tokens = token_set(reference)

    if not reference_tokens:
        return 0.0

    overlap = answer_tokens.intersection(
        reference_tokens
    )

    return len(overlap) / len(reference_tokens)