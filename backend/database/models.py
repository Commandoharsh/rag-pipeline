from dataclasses import dataclass
from datetime import datetime


@dataclass
class DocumentRecord:

    id: str
    filename: str
    file_path: str
    file_type: str
    file_size: int
    status: str
    chunk_count: int
    created_at: datetime
    updated_at: datetime
    error_message: str | None = None