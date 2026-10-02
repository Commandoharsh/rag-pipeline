from backend.evaluation.answer_relevance import (
    answer_relevance_score,
)


def test_answer_relevance():

    score = answer_relevance_score(
        "What is retrieval?",
        "Retrieval finds relevant documents."
    )

    assert score > 0.0