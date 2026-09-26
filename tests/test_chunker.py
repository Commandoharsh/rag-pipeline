from backend.rag.ingestion.document import Document
from backend.rag.chunking.chunker import Chunker


def test_chunker():

    text = (
        "A" * 100
        + "B" * 100
        + "C" * 100
        + "D" * 100
    )

    document = Document(
        content=text,
        metadata={
            "source": "test.txt",
            "page": "1"
        }
    )

    chunker = Chunker(
        chunk_size=150,
        chunk_overlap=50
    )

    chunks = chunker.chunk_document(document)

    assert len(chunks) > 1

    assert chunks[0].content

    assert chunks[0].metadata["source"] == "test.txt"

    assert chunks[0].metadata["page"] == "1"

    assert chunks[0].metadata["chunk_index"] == "0"


def test_chunk_overlap():

    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 20

    document = Document(
        content=text,
        metadata={
            "source": "overlap_test.txt",
            "page": "1"
        }
    )

    chunker = Chunker(
        chunk_size=100,
        chunk_overlap=20
    )

    chunks = chunker.chunk_document(document)

    assert len(chunks) > 1

    first_chunk = chunks[0].content
    second_chunk = chunks[1].content

    # The last 20 characters of the first chunk
    # should appear at the beginning of the second.
    assert first_chunk[-20:] == second_chunk[:20]


def test_invalid_overlap():

    try:
        Chunker(
            chunk_size=100,
            chunk_overlap=100
        )

        assert False

    except ValueError:
        assert True