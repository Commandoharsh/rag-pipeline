import pytest

from backend.rag.query.query_preprocessor import QueryPreprocessor


def test_query_preprocessor():

    processor = QueryPreprocessor()

    result = processor.preprocess(
        "   What   is   RAG???   "
    )

    assert result == "What is RAG?"


def test_empty_query():

    processor = QueryPreprocessor()

    with pytest.raises(ValueError):
        processor.preprocess("")