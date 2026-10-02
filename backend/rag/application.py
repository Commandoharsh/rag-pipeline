from pathlib import Path

from backend.config import settings

# Database
from backend.database.database import Database
from backend.database.document_repository import (
    DocumentRepository,
)
from backend.database.document_service import (
    DocumentService,
)

# RAG state and indexing
from backend.rag.application_state import (
    ApplicationState,
)
from backend.rag.indexing.indexing_pipeline import (
    IndexingPipeline,
)

# Retrieval
from backend.rag.retrieval.retriever import (
    SemanticRetriever,
)
from backend.rag.retrieval.hybrid_retriever import (
    HybridRetriever,
)
from backend.rag.retrieval.reranker import (
    Reranker,
)
from backend.rag.retrieval.reranking_pipeline import (
    RerankingPipeline,
)

# Generation
from backend.rag.generation.answer_generator import (
    AnswerGenerator,
)
from backend.rag.generation.ollama_provider import (
    OllamaProvider,
)

# RAG service
from backend.rag.rag_service import (
    RAGService,
)


class RAGApplication:

    def __init__(self):

        # --------------------------------------------------
        # Application state
        # --------------------------------------------------

        self.state = ApplicationState()

        # --------------------------------------------------
        # Database
        # --------------------------------------------------

        self.database = Database()

        self.document_repository = (
            DocumentRepository(
                self.database
            )
        )

        self.document_service = (
            DocumentService(
                self.document_repository
            )
        )

        # --------------------------------------------------
        # Indexing pipeline
        # --------------------------------------------------

        self.indexing_pipeline = (
            IndexingPipeline(
                embedding_model=(
                    self.state.embedding_model
                ),
                vector_store=(
                    self.state.vector_store
                ),
                bm25_retriever=(
                    self.state.bm25_retriever
                ),
            )
        )

        # --------------------------------------------------
        # Semantic retrieval
        # --------------------------------------------------

        self.semantic_retriever = (
            SemanticRetriever(
                embedding_model=(
                    self.state.embedding_model
                ),
                vector_store=(
                    self.state.vector_store
                ),
            )
        )

        # --------------------------------------------------
        # Hybrid retrieval
        # --------------------------------------------------

        self.hybrid_retriever = (
            HybridRetriever(
                semantic_retriever=(
                    self.semantic_retriever
                ),
                bm25_retriever=(
                    self.state.bm25_retriever
                ),
            )
        )

        # --------------------------------------------------
        # Reranking
        # --------------------------------------------------

        self.reranker = Reranker()

        self.reranking_pipeline = (
            RerankingPipeline(
                retriever=self.hybrid_retriever,
                reranker=self.reranker,
            )
        )

        # --------------------------------------------------
        # LLM
        # --------------------------------------------------

        self.llm = OllamaProvider(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
        )

        # --------------------------------------------------
        # Answer generation
        # --------------------------------------------------

        self.answer_generator = (
            AnswerGenerator(
                llm=self.llm
            )
        )

        # --------------------------------------------------
        # Main RAG service
        # --------------------------------------------------

        self.rag_service = RAGService(
            retriever=self.reranking_pipeline,
            answer_generator=self.answer_generator,
        )

    # ======================================================
    # DOCUMENT INDEXING
    # ======================================================

    def index_pdf(
        self,
        file_path: str,
    ):

        path = Path(file_path)

        # --------------------------------------------------
        # Validate file
        # --------------------------------------------------

        if not path.exists():

            raise FileNotFoundError(
                f"PDF file not found: {file_path}"
            )

        if not path.is_file():

            raise ValueError(
                f"Path is not a file: {file_path}"
            )

        if path.suffix.lower() != ".pdf":

            raise ValueError(
                "Only PDF files are supported."
            )

        # --------------------------------------------------
        # Register document
        # --------------------------------------------------

        document = (
            self.document_service.register(
                filename=path.name,
                file_path=str(path),
                file_size=path.stat().st_size,
                file_type="pdf",
            )
        )

        try:

            # --------------------------------------------------
            # Mark indexing started
            # --------------------------------------------------

            self.document_service.mark_indexing(
                document.id
            )

            # --------------------------------------------------
            # Run indexing pipeline
            # --------------------------------------------------

            result = (
                self.indexing_pipeline.index_pdf(
                    str(path)
                )
            )

            # --------------------------------------------------
            # Mark indexing successful
            # --------------------------------------------------

            self.document_service.mark_indexed(
                document.id,
                result["chunks"],
            )

            # --------------------------------------------------
            # Add document ID to result
            # --------------------------------------------------

            result["document_id"] = (
                document.id
            )

            result["status"] = "indexed"

            return result

        except Exception as exc:

            # --------------------------------------------------
            # Mark indexing failed
            # --------------------------------------------------

            self.document_service.mark_failed(
                document.id,
                str(exc),
            )

            raise

    # ======================================================
    # QUERY
    # ======================================================

    def query(
        self,
        question: str,
        conversation_context=None,
    ):

        return self.rag_service.query(
            question=question,
            conversation_context=(
                conversation_context
            ),
        )

    # ======================================================
    # DOCUMENT MANAGEMENT
    # ======================================================

    def get_document(
        self,
        document_id: str,
    ):

        return self.document_repository.get(
            document_id
        )

    def list_documents(self):

        return self.document_repository.list()

    def delete_document_record(
        self,
        document_id: str,
    ):

        self.document_repository.delete(
            document_id
        )

    # ======================================================
    # SHUTDOWN
    # ======================================================

    def close(self):

        self.state.close()


# ==========================================================
# APPLICATION SINGLETON
# ==========================================================

_application = None


def create_rag_application():

    global _application

    if _application is None:

        _application = RAGApplication()

    return _application