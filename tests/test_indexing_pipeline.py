from pathlib import Path

from reportlab.pdfgen import canvas

from backend.rag.embeddings.embedding_model import EmbeddingModel
from backend.rag.indexing.indexing_pipeline import IndexingPipeline
from backend.rag.retrieval.bm25_retriever import BM25Retriever
from backend.rag.retrieval.vector_store import VectorStore


def create_test_pdf(file_path: Path):

    pdf = canvas.Canvas(str(file_path))

    pdf.drawString(
        100,
        750,
        "Retrieval augmented generation combines "
        "information retrieval with language models."
    )

    pdf.drawString(
        100,
        730,
        "RAG systems retrieve relevant documents "
        "before generating an answer."
    )

    pdf.save()


def test_indexing_pipeline(tmp_path):

    pdf_path = tmp_path / "test.pdf"

    create_test_pdf(pdf_path)

    vector_store = VectorStore(
        collection_name="test_collection",
        vector_size=384,
        storage_path=str(
            tmp_path / "qdrant"
        )
    )

    embedding_model = EmbeddingModel()

    bm25_retriever = BM25Retriever()

    pipeline = IndexingPipeline(
        embedding_model=embedding_model,
        vector_store=vector_store,
        bm25_retriever=bm25_retriever
    )

    result = pipeline.index_pdf(
        str(pdf_path)
    )

    assert result["file"] == "test.pdf"

    assert result["documents"] == 1

    assert result["chunks"] > 0

    assert result["total_indexed_chunks"] > 0

    assert result["embedding_dimension"] == 384

    vector_store.close()