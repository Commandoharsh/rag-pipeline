from backend.rag.ingestion.document import Document
from backend.rag.chunking.chunker import Chunker


class RAGPipeline:

    def __init__(self):

        self.chunker = Chunker(
            chunk_size=1000,
            chunk_overlap=150
        )

    def process_document(
        self,
        document: Document
    ):

        chunks = self.chunker.chunk_document(
            document
        )

        return chunks