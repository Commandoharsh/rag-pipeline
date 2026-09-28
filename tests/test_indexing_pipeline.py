from reportlab.pdfgen import canvas

from backend.rag.indexing.indexing_pipeline import IndexingPipeline


def create_test_pdf(file_path):
    pdf = canvas.Canvas(str(file_path))

    pdf.drawString(
        100,
        750,
        "Artificial intelligence is transforming healthcare."
    )

    pdf.drawString(
        100,
        730,
        "Machine learning can assist doctors in medical diagnosis."
    )

    pdf.drawString(
        100,
        710,
        "Retrieval augmented generation combines retrieval with language models."
    )

    pdf.save()


def test_indexing_pipeline(tmp_path):

    pdf_path = tmp_path / "research.pdf"

    create_test_pdf(pdf_path)

    pipeline = IndexingPipeline(
        chunk_size=200,
        chunk_overlap=30
    )

    result = pipeline.index_pdf(str(pdf_path))

    assert result["file"] == "research.pdf"
    assert result["documents"] == 1
    assert result["chunks"] > 0
    assert result["embedding_dimension"] == 384