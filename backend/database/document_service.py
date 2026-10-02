from datetime import datetime, timezone
from uuid import uuid4

from backend.database.models import DocumentRecord
from backend.database.status import DocumentStatus
from backend.database.document_repository import (
    DocumentRepository,
)


class DocumentService:

    def __init__(
        self,
        repository: DocumentRepository,
    ):
        self.repository = repository

    def register(
        self,
        filename: str,
        file_path: str,
        file_size: int,
        file_type: str = "pdf",
    ):

        now = datetime.now(
            timezone.utc
        )

        document = DocumentRecord(
            id=str(uuid4()),
            filename=filename,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
            status=DocumentStatus.UPLOADED.value,
            chunk_count=0,
            created_at=now,
            updated_at=now,
        )

        return self.repository.create(
            document
        )

    def mark_indexing(
        self,
        document_id: str,
    ):

        self.repository.update_status(
            document_id,
            status="indexing",
        )

    def mark_indexed(
        self,
        document_id: str,
        chunk_count: int,
    ):

        self.repository.update_status(
            document_id,
            status="indexed",
            chunk_count=chunk_count,
        )

    def mark_failed(
        self,
        document_id: str,
        error_message: str,
    ):

        self.repository.update_status(
            document_id,
            status="failed",
            error_message=error_message,
        )
    def get(
    self,
    document_id: str,
    ):
        return self.repository.get(
        document_id
    )


    def list_documents(self):
        return self.repository.list()


def delete(
    self,
    document_id: str,
):
    self.repository.delete(
        document_id
    )