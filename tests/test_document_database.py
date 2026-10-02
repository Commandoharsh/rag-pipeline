from backend.database.database import Database
from backend.database.document_repository import (
    DocumentRepository,
)
from backend.database.document_service import (
    DocumentService,
)


def create_service(tmp_path):

    database = Database(
        str(tmp_path / "test.db")
    )

    repository = DocumentRepository(
        database
    )

    return DocumentService(
        repository
    ), repository


def test_register_document(tmp_path):

    service, repository = (
        create_service(tmp_path)
    )

    document = service.register(
        filename="research.pdf",
        file_path="data/raw/research.pdf",
        file_size=1024,
    )

    assert document.filename == "research.pdf"

    stored = repository.get(
        document.id
    )

    assert stored is not None

    assert (
        stored.filename
        == "research.pdf"
    )


def test_document_status(tmp_path):

    service, repository = (
        create_service(tmp_path)
    )

    document = service.register(
        filename="research.pdf",
        file_path="research.pdf",
        file_size=100,
    )

    service.mark_indexing(
        document.id
    )

    stored = repository.get(
        document.id
    )

    assert stored.status == "indexing"


def test_mark_indexed(tmp_path):

    service, repository = (
        create_service(tmp_path)
    )

    document = service.register(
        filename="research.pdf",
        file_path="research.pdf",
        file_size=100,
    )

    service.mark_indexed(
        document.id,
        25,
    )

    stored = repository.get(
        document.id
    )

    assert stored.status == "indexed"

    assert stored.chunk_count == 25


def test_mark_failed(tmp_path):

    service, repository = (
        create_service(tmp_path)
    )

    document = service.register(
        filename="research.pdf",
        file_path="research.pdf",
        file_size=100,
    )

    service.mark_failed(
        document.id,
        "Test failure",
    )

    stored = repository.get(
        document.id
    )

    assert stored.status == "failed"

    assert (
        stored.error_message
        == "Test failure"
    )