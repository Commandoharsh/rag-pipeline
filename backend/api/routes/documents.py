from fastapi import APIRouter

from backend.database.database import Database
from backend.database.document_repository import (
    DocumentRepository,
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


database = Database()

repository = DocumentRepository(
    database
)


@router.get("")
def list_documents():

    documents = repository.list()

    return {
        "documents": [
            {
                "id": document.id,
                "filename": document.filename,
                "file_type": document.file_type,
                "file_size": document.file_size,
                "status": document.status,
                "chunk_count": document.chunk_count,
                "created_at": document.created_at,
                "updated_at": document.updated_at,
                "error_message": document.error_message,
            }
            for document in documents
        ]
    }


@router.get("/{document_id}")
def get_document(
    document_id: str,
):

    document = repository.get(
        document_id
    )

    if document is None:

        return {
            "error": "Document not found"
        }

    return {
        "id": document.id,
        "filename": document.filename,
        "file_type": document.file_type,
        "file_size": document.file_size,
        "status": document.status,
        "chunk_count": document.chunk_count,
        "created_at": document.created_at,
        "updated_at": document.updated_at,
        "error_message": document.error_message,
    }
    