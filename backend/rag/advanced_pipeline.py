from backend.rag.query.query_intent import (
    QueryIntentClassifier,
)

from backend.rag.query.llm_query_rewriter import (
    LLMQueryRewriter,
)

from backend.rag.query.llm_multi_query import (
    LLMMultiQueryGenerator,
)

from backend.rag.retrieval.adaptive_retriever import (
    AdaptiveRetriever,
)

from backend.rag.retrieval.metadata_filter import (
    MetadataFilter,
)

from backend.rag.generation.llm_context_compressor import (
    LLMContextCompressor,
)


class AdvancedRAGPipeline:

    def __init__(
        self,
        llm,
        retriever,
    ):

        self.intent_classifier = (
            QueryIntentClassifier()
        )

        self.query_rewriter = (
            LLMQueryRewriter(llm)
        )

        self.multi_query_generator = (
            LLMMultiQueryGenerator(llm)
        )

        self.retriever = AdaptiveRetriever(
            retriever
        )

        self.metadata_filter = (
            MetadataFilter()
        )

        self.context_compressor = (
            LLMContextCompressor(llm)
        )

    def retrieve(
        self,
        question: str,
        metadata_filter: dict | None = None,
        conversation_context: str | None = None,
    ):

        intent = self.intent_classifier.classify(
            question
        )

        rewritten = self.query_rewriter.rewrite(
            question,
            conversation_context,
        )

        queries = (
            self.multi_query_generator.generate(
                rewritten
            )
        )

        all_results = []

        for query in queries:

            results = self.retriever.retrieve(
                query,
                intent,
            )

            all_results.extend(results)

        results = self.metadata_filter.filter(
            all_results,
            metadata_filter,
        )

        return {
            "intent": intent.value,
            "rewritten_query": rewritten,
            "queries": queries,
            "results": results,
        }

    def compress_context(
        self,
        question: str,
        results,
    ):

        compressed = []

        for result in results:

            result.content = (
                self.context_compressor.compress(
                    question,
                    result.content,
                )
            )

            compressed.append(result)

        return compressed