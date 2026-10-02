from backend.evaluation.answer_metrics import (
    answer_keyword_overlap,
)


def test_answer_keyword_overlap():

    score = answer_keyword_overlap(
        "RAG uses retrieval and generation.",
        "RAG uses retrieval and generation."
    )

    assert score == 1.0