from backend.rag.generation.citation_extractor import CitationExtractor


def test_citation_extractor():

    extractor = CitationExtractor()

    answer = (
        "RAG combines retrieval and generation "
        "[SOURCE 1]. It can use external knowledge "
        "[SOURCE 2]."
    )

    citations = extractor.extract(answer)

    assert citations == [1, 2]