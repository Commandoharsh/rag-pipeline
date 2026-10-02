from backend.rag.query.query_intent import (
    QueryIntent,
    QueryIntentClassifier,
)

from backend.rag.retrieval.metadata_filter import (
    MetadataFilter,
)


def test_definition_intent():

    classifier = QueryIntentClassifier()

    result = classifier.classify(
        "What is retrieval augmented generation?"
    )

    assert result == QueryIntent.DEFINITION


def test_comparison_intent():

    classifier = QueryIntentClassifier()

    result = classifier.classify(
        "What is the difference between BM25 and dense retrieval?"
    )

    assert result == QueryIntent.COMPARISON


def test_analytical_intent():

    classifier = QueryIntentClassifier()

    result = classifier.classify(
        "Why does reranking improve retrieval?"
    )

    assert result == QueryIntent.ANALYTICAL


def test_metadata_filter():

    class Result:

        def __init__(self, source):
            self.metadata = {
                "source": source
            }

    results = [
        Result("paper_a.pdf"),
        Result("paper_b.pdf"),
    ]

    filterer = MetadataFilter()

    filtered = filterer.filter(
        results,
        {
            "source": "paper_a.pdf"
        },
    )

    assert len(filtered) == 1

    assert (
        filtered[0].metadata["source"]
        == "paper_a.pdf"
    )


def test_metadata_filter_without_filter():

    filterer = MetadataFilter()

    results = [1, 2, 3]

    assert (
        filterer.filter(results)
        == results
    )