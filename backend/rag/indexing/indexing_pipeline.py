from pathlib import Path

from backend.rag.ingestion.pdf_loader import PDFLoader
from backend.rag.chunking.chunker import Chunker
from backend.rag.embeddings.embedding_model import EmbeddingModel
from backend.rag.retrieval.vector_store import VectorStore


class IndexingPipeline:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 150,
        embedding_model: str = "all-MiniLM-L6-v2",
    ):
        self.pdf_loader = PDFLoader()

        self.chunker = Chunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        self.embedding_model = EmbeddingModel(
            model_name=embedding_model
        )

        self.vector_store = VectorStore(
            vector_size=384
        )

    def index_pdf(self, file_path: str):
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {file_path}"
            )

        # 1. Load PDF
        documents = self.pdf_loader.load(str(path))

        # 2. Chunk documents
        all_chunks = []

        for document in documents:
            chunks = self.chunker.chunk_document(document)
            all_chunks.extend(chunks)

        if not all_chunks:
            raise ValueError(
                "No text chunks were generated from the PDF."
            )

        # 3. Generate embeddings
        texts = [chunk.content for chunk in all_chunks]

        embeddings = self.embedding_model.encode(texts)

        # 4. Store vectors in Qdrant
        self.vector_store.add_chunks(
            all_chunks,
            embeddings
        )

        return {
            "file": path.name,
            "documents": len(documents),
            "chunks": len(all_chunks),
            "embedding_dimension": embeddings.shape[1],
        }