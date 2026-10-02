from backend.rag.generation.citation_validator import CitationValidator


def test_citation_validator():

    validator = CitationValidator()

    result = validator.validate(
        citation_ids=[1, 2, 5, 10],
        source_count=3
    )

    assert result == [1, 2]