from backend.evaluation.retrieval_metrics import (
    recall_at_k,
    reciprocal_rank,
    ndcg_at_k,
)


class RetrievalEvaluator:

    def evaluate_case(
        self,
        retrieved_results,
        relevant_chunks: set[str],
    ):
        retrieved_ids = [
            result.chunk_id
            for result in retrieved_results
        ]

        return {
            "recall@1": recall_at_k(
                retrieved_ids,
                relevant_chunks,
                1,
            ),
            "recall@3": recall_at_k(
                retrieved_ids,
                relevant_chunks,
                3,
            ),
            "recall@5": recall_at_k(
                retrieved_ids,
                relevant_chunks,
                5,
            ),
            "mrr": reciprocal_rank(
                retrieved_ids,
                relevant_chunks,
            ),
            "ndcg@5": ndcg_at_k(
                retrieved_ids,
                relevant_chunks,
                5,
            ),
        }

    def evaluate(
        self,
        retriever,
        dataset,
        top_k: int = 5,
    ):
        case_results = []

        for case in dataset:

            retrieved = retriever.retrieve(
                case.question,
                top_k=top_k,
            )

            metrics = self.evaluate_case(
                retrieved,
                case.relevant_chunks,
            )

            case_results.append(
                {
                    "id": case.id,
                    "question": case.question,
                    "retrieved_chunks": [
                        result.chunk_id
                        for result in retrieved
                    ],
                    "metrics": metrics,
                }
            )

        return self._aggregate(case_results)

    def _aggregate(self, case_results):

        if not case_results:
            return {
                "cases": [],
                "metrics": {},
            }

        metric_names = [
            "recall@1",
            "recall@3",
            "recall@5",
            "mrr",
            "ndcg@5",
        ]

        averages = {}

        for metric in metric_names:
            values = [
                case["metrics"][metric]
                for case in case_results
            ]

            averages[metric] = (
                sum(values) / len(values)
            )

        return {
            "cases": case_results,
            "metrics": averages,
        }