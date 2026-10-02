from enum import Enum


class DocumentStatus(str, Enum):

    UPLOADED = "uploaded"

    INDEXING = "indexing"

    INDEXED = "indexed"

    FAILED = "failed"

    DELETING = "deleting"