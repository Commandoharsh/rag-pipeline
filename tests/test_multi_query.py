from backend.rag.query.multi_query import MultiQueryGenerator


def test_multi_query():

    generator = MultiQueryGenerator()

    queries = generator.generate(
        "retrieval augmented generation",
        num_queries=3
    )

    assert len(queries) == 3
    assert all(queries)