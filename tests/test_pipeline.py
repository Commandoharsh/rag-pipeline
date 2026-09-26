from backend.rag.ingestion.document import Document
from backend.rag.chunking.chunker import Chunker


def test_document_to_chunks():

    document = Document(
        content="""
        Retrieval-Augmented Generation combines
        information retrieval with language models.

        The retrieval system searches a knowledge base
        for relevant information.

        The language model then uses the retrieved
        information to generate a grounded response.
        """,
        metadata={
            "source": "rag_intro.txt",
            "page": "1",
            "file_type": "text"
        }
    )

    chunker = Chunker(
        chunk_size=150,
        chunk_overlap=30
    )

    chunks = chunker.chunk_document(document)

    assert len(chunks) > 1

    for chunk in chunks:

        assert chunk.content

        assert chunk.metadata["source"] == "rag_intro.txt"

        assert "chunk_index" in chunk.metadata

        assert "chunk_size" in chunk.metadata