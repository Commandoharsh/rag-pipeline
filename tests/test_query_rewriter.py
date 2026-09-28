from backend.rag.query.query_rewriter import QueryRewriter


def test_query_rewriter():

    rewriter = QueryRewriter()

    result = rewriter.rewrite(
        "How does it work?",
        "We are discussing Retrieval Augmented Generation."
    )

    assert "Retrieval Augmented Generation" in result
    assert "How does it work?" in result


def test_query_without_context():

    rewriter = QueryRewriter()

    result = rewriter.rewrite(
        "What is RAG?"
    )

    assert result == "What is RAG?"