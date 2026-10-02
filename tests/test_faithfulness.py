from backend.evaluation.faithfulness import faithfulness_score


def test_faithfulness():

    score = faithfulness_score(
        "RAG uses retrieval.",
        "RAG uses retrieval to find relevant information."
    )

    assert score > 0.5