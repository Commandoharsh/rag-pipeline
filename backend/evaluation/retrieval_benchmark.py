from backend.evaluation.dataset import EVALUATION_DATASET
from backend.evaluation.retrieval_evaluator import RetrievalEvaluator


class RetrievalBenchmark:

    def __init__(self, application):
        self.application = application
        self.evaluator = RetrievalEvaluator()

    def run(self):

        strategies = {
            "semantic": self.application.semantic_retriever,
            "bm25": self.application.bm25_retriever,
            "hybrid": self.application.hybrid_retriever,
            "hybrid_reranker": self.application.reranking_pipeline,
        }

        results = {}

        for name, retriever in strategies.items():

            print(
                f"Evaluating retrieval strategy: {name}"
            )

            results[name] = self.evaluator.evaluate(
                retriever=retriever,
                dataset=EVALUATION_DATASET,
                top_k=5,
            )

        return results