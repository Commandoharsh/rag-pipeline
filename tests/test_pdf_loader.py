from pathlib import Path

from reportlab.pdfgen import canvas

from backend.rag.ingestion.pdf_loader import PDFLoader


def create_test_pdf(file_path: Path):

    pdf = canvas.Canvas(str(file_path))

    pdf.drawString(
        100,
        750,
        "ResearchRAG is an intelligent research platform."
    )

    pdf.drawString(
        100,
        730,
        "This document is used to test PDF ingestion."
    )

    pdf.save()


def test_pdf_loader(tmp_path):

    pdf_path = tmp_path / "sample.pdf"

    create_test_pdf(pdf_path)

    loader = PDFLoader()

    documents = loader.load(str(pdf_path))

    assert len(documents) == 1

    assert documents[0].content

    assert "ResearchRAG" in documents[0].content

    assert documents[0].metadata["source"] == "sample.pdf"

    assert documents[0].metadata["page"] == "1"

    assert documents[0].metadata["file_type"] == "pdf"