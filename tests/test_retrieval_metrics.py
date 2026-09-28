from backend.evaluation.retrieval_metrics import (
    recall_at_k,
    reciprocal_rank,
    mean_reciprocal_rank,
    ndcg_at_k,
)


def test_recall_at_k():

    retrieved = ["A", "B", "C", "D"]
    relevant = {"A", "C", "E"}

    score = recall_at_k(
        retrieved,
        relevant,
        k=4
    )

    assert score == 2 / 3


def test_reciprocal_rank():

    retrieved = ["A", "B", "C"]
    relevant = {"B"}

    score = reciprocal_rank(
        retrieved,
        relevant
    )

    assert score == 0.5


def test_mrr():

    retrieved = [
        ["A", "B", "C"],
        ["D", "E", "F"],
        ["X", "Y", "Z"]
    ]

    relevant = [
        {"A"},
        {"E"},
        {"Q"}
    ]

    score = mean_reciprocal_rank(
        retrieved,
        relevant
    )

    assert score == (1.0 + 0.5 + 0.0) / 3


def test_ndcg():

    retrieved = ["A", "B", "C"]
    relevant = {"A", "B"}

    score = ndcg_at_k(
        retrieved,
        relevant,
        k=3
    )

    assert 0.0 <= score <= 1.0