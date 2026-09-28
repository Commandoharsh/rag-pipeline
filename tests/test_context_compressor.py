from backend.rag.generation.context_compressor import ContextCompressor


def test_context_compression():

    compressor = ContextCompressor()

    result = compressor.compress(
        "machine learning healthcare",
        (
            "Machine learning is used in healthcare. "
            "The solar system contains planets. "
            "Healthcare models can assist diagnosis."
        )
    )

    assert "Machine learning" in result
    assert "healthcare" in result.lower()