from backend.evaluation.retrieval_metrics import (
    recall_at_k,
    reciprocal_rank,
    ndcg_at_k,
)

from backend.evaluation.answer_metrics import (
    answer_keyword_overlap,
)

from backend.evaluation.answer_relevance import (
    answer_relevance_score,
)

from backend.evaluation.faithfulness import (
    faithfulness_score,
)


def test_recall_at_k():

    retrieved = [
        "a",
        "b",
        "c",
    ]

    relevant = {
        "b",
        "c",
    }

    assert recall_at_k(
        retrieved,
        relevant,
        3,
    ) == 1.0


def test_reciprocal_rank():

    retrieved = [
        "a",
        "b",
        "c",
    ]

    relevant = {
        "b",
    }

    assert reciprocal_rank(
        retrieved,
        relevant,
    ) == 0.5


def test_ndcg_at_k():

    retrieved = [
        "a",
        "b",
        "c",
    ]

    relevant = {
        "b",
    }

    score = ndcg_at_k(
        retrieved,
        relevant,
        3,
    )

    assert 0.0 <= score <= 1.0


def test_answer_keyword_overlap():

    score = answer_keyword_overlap(
        "machine learning improves prediction",
        "machine learning improves prediction accuracy",
    )

    assert 0.0 < score <= 1.0


def test_answer_relevance():

    score = answer_relevance_score(
        "What is machine learning?",
        "Machine learning is a method for learning from data.",
    )

    assert 0.0 <= score <= 1.0


def test_faithfulness():

    score = faithfulness_score(
        "machine learning uses data",
        "machine learning uses data to make predictions",
    )

    assert 0.0 < score <= 1.0


def test_empty_relevant_set():

    assert recall_at_k(
        ["a", "b"],
        set(),
        5,
    ) == 0.0


def test_empty_retrieval():

    assert reciprocal_rank(
        [],
        {"a"},
    ) == 0.0


def test_empty_reference():

    assert answer_keyword_overlap(
        "some answer",
        "",
    ) == 0.0