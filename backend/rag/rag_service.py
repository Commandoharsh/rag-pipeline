import time

from backend.config import settings

from backend.rag.query.query_preprocessor import QueryPreprocessor
from backend.rag.query.query_rewriter import QueryRewriter
from backend.rag.query.multi_query import MultiQueryGenerator

from backend.rag.retrieval.rrf import reciprocal_rank_fusion
from backend.rag.retrieval.deduplicator import ResultDeduplicator

from backend.rag.generation.answer_generator import AnswerGenerator
from backend.rag.generation.citation_service import CitationService
from backend.rag.generation.context_compressor import ContextCompressor
from backend.rag.generation.context_orderer import ContextOrderer
from backend.rag.generation.context_builder import ContextBuilder

from backend.rag.metrics import RAGMetrics


class RAGService:
    """
    Main orchestration layer for the ResearchRAG pipeline.

    Pipeline:

        Question
            ↓
        Preprocessing
            ↓
        Query Rewriting
            ↓
        Multi Query Generation
            ↓
        Retrieval
            ↓
        Reciprocal Rank Fusion
            ↓
        Deduplication
            ↓
        Context Ordering
            ↓
        Context Compression
            ↓
        Context Building
            ↓
        LLM Generation
            ↓
        Citation Generation
    """

    def __init__(
        self,
        retriever,
        answer_generator: AnswerGenerator,
    ):
        self.retriever = retriever
        self.answer_generator = answer_generator

        self.query_preprocessor = QueryPreprocessor()
        self.query_rewriter = QueryRewriter()
        self.multi_query_generator = MultiQueryGenerator()

        self.deduplicator = ResultDeduplicator()

        self.context_compressor = ContextCompressor()
        self.context_orderer = ContextOrderer()
        self.context_builder = ContextBuilder()

        self.citation_service = CitationService()

        # Stores metrics from the most recent query.
        self.last_metrics = RAGMetrics()

    def prepare(
        self,
        question: str,
        conversation_context: str | None = None,
    ):
        """
        Runs the retrieval/context preparation portion
        of the RAG pipeline.
        """

        metrics = RAGMetrics()

        total_start = time.perf_counter()

        # -------------------------------------------------
        # 1. Query preprocessing
        # -------------------------------------------------

        start = time.perf_counter()

        question = self.query_preprocessor.preprocess(question)

        metrics.preprocessing_ms = (
            time.perf_counter() - start
        ) * 1000

        # -------------------------------------------------
        # 2. Query rewriting
        # -------------------------------------------------

        start = time.perf_counter()

        rewritten_query = self.query_rewriter.rewrite(
            question,
            conversation_context,
        )

        metrics.rewriting_ms = (
            time.perf_counter() - start
        ) * 1000

        # -------------------------------------------------
        # 3. Multi-query generation
        # -------------------------------------------------

        start = time.perf_counter()

        queries = self.multi_query_generator.generate(
            rewritten_query,
            num_queries=3,
        )

        # Multi-query generation is currently included
        # in the rewriting stage because it is part of
        # query transformation.
        metrics.rewriting_ms += (
            time.perf_counter() - start
        ) * 1000

        # -------------------------------------------------
        # 4. Retrieval
        # -------------------------------------------------

        start = time.perf_counter()

        all_results = []

        for generated_query in queries:
            results = self.retriever.retrieve(
                generated_query,
                retrieval_k=settings.RAG_RETRIEVAL_K,
                final_k=settings.RAG_RETRIEVAL_K,
            )

            all_results.append(results)

        metrics.retrieval_ms = (
            time.perf_counter() - start
        ) * 1000

        metrics.retrieved_documents = sum(
            len(results)
            for results in all_results
        )

        # -------------------------------------------------
        # 5. Reciprocal Rank Fusion
        # -------------------------------------------------

        start = time.perf_counter()

        results = reciprocal_rank_fusion(
            all_results,
            top_k=settings.RAG_TOP_K,
        )

        metrics.fusion_ms = (
            time.perf_counter() - start
        ) * 1000

        # -------------------------------------------------
        # 6. Deduplication
        # -------------------------------------------------

        results = self.deduplicator.deduplicate(results)

        # -------------------------------------------------
        # 7. Context ordering
        # -------------------------------------------------

        results = self.context_orderer.order(results)

        # -------------------------------------------------
        # 8. Context compression
        # -------------------------------------------------

        start = time.perf_counter()

        for result in results:
            result.content = self.context_compressor.compress(
                rewritten_query,
                result.content,
            )

        metrics.compression_ms = (
            time.perf_counter() - start
        ) * 1000

        metrics.final_documents = len(results)

        # -------------------------------------------------
        # 9. Context construction
        # -------------------------------------------------

        context = self.context_builder.build(results)

        metrics.total_ms = (
            time.perf_counter() - total_start
        ) * 1000

        self.last_metrics = metrics

        return {
            "question": question,
            "rewritten_query": rewritten_query,
            "queries": queries,
            "results": results,
            "context": context,
            "metrics": metrics,
        }

    def query(
        self,
        question: str,
        conversation_context: str | None = None,
    ):
        """
        Executes the complete RAG pipeline.
        """

        total_start = time.perf_counter()

        prepared = self.prepare(
            question=question,
            conversation_context=conversation_context,
        )

        # -------------------------------------------------
        # LLM generation
        # -------------------------------------------------

        generation_start = time.perf_counter()

        answer = self.answer_generator.generate(
            question=prepared["question"],
            context=prepared["context"],
        )

        generation_ms = (
            time.perf_counter() - generation_start
        ) * 1000

        # -------------------------------------------------
        # Citation generation
        # -------------------------------------------------

        response = self.citation_service.build_response(
            answer=answer,
            results=prepared["results"],
        )

        # Update metrics with generation time.
        metrics = prepared["metrics"]

        metrics.generation_ms = generation_ms
        metrics.total_ms = (
            time.perf_counter() - total_start
        ) * 1000

        self.last_metrics = metrics

        return {
            "question": prepared["question"],
            "rewritten_query": prepared["rewritten_query"],
            "queries": prepared["queries"],
            "answer": response.answer,
            "citations": response.citations,
            "results": prepared["results"],
            "context": prepared["context"],
            "metrics": metrics,
        }