from backend.rag.ingestion.document import Document
from backend.rag.chunking.chunk import Chunk
from backend.rag.chunking.text_cleaner import TextCleaner


class Chunker:

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 150
    ):
        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_document(
        self,
        document: Document
    ) -> list[Chunk]:

        text = TextCleaner.clean(document.content)

        if not text:
            return []

        chunks = []

        start = 0
        chunk_index = 0
        text_length = len(text)

        while start < text_length:

            end = min(
                start + self.chunk_size,
                text_length
            )

            chunk_text = text[start:end].strip()

            if chunk_text:

                chunks.append(
                    self._create_chunk(
                        chunk_text,
                        document,
                        chunk_index
                    )
                )

                chunk_index += 1

            if end >= text_length:
                break

            start = end - self.chunk_overlap

        return chunks

    def _create_chunk(
        self,
        content: str,
        document: Document,
        chunk_index: int
    ) -> Chunk:

        metadata = document.metadata.copy()

        metadata["chunk_index"] = str(chunk_index)

        metadata["chunk_size"] = str(len(content))

        return Chunk(
            content=content,
            metadata=metadata
        )