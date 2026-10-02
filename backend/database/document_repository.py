from datetime import datetime, timezone

from backend.database.database import Database
from backend.database.models import DocumentRecord


class DocumentRepository:

    def __init__(self, database: Database):

        self.database = database

    def create(
        self,
        document: DocumentRecord,
    ):

        with self.database._connect() as connection:

            connection.execute(
                """
                INSERT INTO documents (
                    id,
                    filename,
                    file_path,
                    file_type,
                    file_size,
                    status,
                    chunk_count,
                    created_at,
                    updated_at,
                    error_message
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    document.id,
                    document.filename,
                    document.file_path,
                    document.file_type,
                    document.file_size,
                    document.status,
                    document.chunk_count,
                    document.created_at.isoformat(),
                    document.updated_at.isoformat(),
                    document.error_message,
                ),
            )

            connection.commit()

        return document

    def get(self, document_id: str):

        with self.database._connect() as connection:

            row = connection.execute(
                """
                SELECT *
                FROM documents
                WHERE id = ?
                """,
                (document_id,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_document(row)

    def list(self):

        with self.database._connect() as connection:

            rows = connection.execute(
                """
                SELECT *
                FROM documents
                ORDER BY created_at DESC
                """
            ).fetchall()

        return [
            self._row_to_document(row)
            for row in rows
        ]

    def update_status(
        self,
        document_id: str,
        status: str,
        chunk_count: int | None = None,
        error_message: str | None = None,
    ):

        updated_at = datetime.now(
            timezone.utc
        ).isoformat()

        with self.database._connect() as connection:

            if chunk_count is None:

                connection.execute(
                    """
                    UPDATE documents
                    SET
                        status = ?,
                        updated_at = ?,
                        error_message = ?
                    WHERE id = ?
                    """,
                    (
                        status,
                        updated_at,
                        error_message,
                        document_id,
                    ),
                )

            else:

                connection.execute(
                    """
                    UPDATE documents
                    SET
                        status = ?,
                        chunk_count = ?,
                        updated_at = ?,
                        error_message = ?
                    WHERE id = ?
                    """,
                    (
                        status,
                        chunk_count,
                        updated_at,
                        error_message,
                        document_id,
                    ),
                )

            connection.commit()

    def delete(
        self,
        document_id: str,
    ):

        with self.database._connect() as connection:

            connection.execute(
                """
                DELETE FROM documents
                WHERE id = ?
                """,
                (document_id,),
            )

            connection.commit()

    @staticmethod
    def _row_to_document(row):

        return DocumentRecord(
            id=row["id"],
            filename=row["filename"],
            file_path=row["file_path"],
            file_type=row["file_type"],
            file_size=row["file_size"],
            status=row["status"],
            chunk_count=row["chunk_count"],
            created_at=datetime.fromisoformat(
                row["created_at"]
            ),
            updated_at=datetime.fromisoformat(
                row["updated_at"]
            ),
            error_message=row["error_message"],
        )
        