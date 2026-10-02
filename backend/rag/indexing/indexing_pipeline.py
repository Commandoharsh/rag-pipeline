from pathlib import Path

from backend.rag.ingestion.pdf_loader import PDFLoader
from backend.rag.chunking.chunker import Chunker
from backend.rag.embeddings.embedding_model import EmbeddingModel
from backend.rag.retrieval.vector_store import VectorStore
from backend.rag.retrieval.bm25_retriever import BM25Retriever


class IndexingPipeline:

    def __init__(
        self,
        embedding_model=None,
        vector_store=None,
        bm25_retriever=None,
        chunk_size: int = 1000,
        chunk_overlap: int = 150
    ):

        self.pdf_loader = PDFLoader()

        self.chunker = Chunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        self.embedding_model = (
            embedding_model
            or EmbeddingModel()
        )

        self.vector_store = (
            vector_store
            or VectorStore()
        )

        self.bm25_retriever = (
            bm25_retriever
            or BM25Retriever()
        )

    def index_pdf(
        self,
        file_path: str
    ):

        path = Path(file_path)

        if not path.exists():

            raise FileNotFoundError(
                f"PDF file not found: {file_path}"
            )

        documents = self.pdf_loader.load(
            str(path)
        )

        all_chunks = []

        for document in documents:

            chunks = self.chunker.chunk_document(
                document
            )

            all_chunks.extend(chunks)

        if not all_chunks:

            raise ValueError(
                "No text chunks were generated "
                "from the PDF."
            )

        texts = [
            chunk.content
            for chunk in all_chunks
        ]

        embeddings = self.embedding_model.encode(
            texts
        )

        self.vector_store.add_chunks(
            all_chunks,
            embeddings
        )

        # Rebuild BM25 using everything currently
        # stored in Qdrant.
        all_indexed_chunks = (
            self.vector_store.get_all_chunks()
        )

        self.bm25_retriever.index(
            all_indexed_chunks
        )

        return {
            "file": path.name,
            "documents": len(documents),
            "chunks": len(all_chunks),
            "total_indexed_chunks": len(
                all_indexed_chunks
            ),
            "embedding_dimension": embeddings.shape[1]
        }