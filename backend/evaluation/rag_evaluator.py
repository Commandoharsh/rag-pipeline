from backend.evaluation.answer_metrics import (
    answer_keyword_overlap,
)

from backend.evaluation.answer_relevance import (
    answer_relevance_score,
)

from backend.evaluation.faithfulness import (
    faithfulness_score,
)


class RAGEvaluator:

    # ---------------------------------------------------------
    # Backward-compatible single evaluation
    # ---------------------------------------------------------

    def evaluate(
        self,
        question: str | None = None,
        answer: str | None = None,
        reference_answer: str | None = None,
        context: str | None = None,
        rag_service=None,
        dataset=None,
    ):
        """
        Supports two evaluation modes.

        Mode 1:
            evaluate(
                question=...,
                answer=...,
                reference_answer=...,
                context=...
            )

        Mode 2:
            evaluate(
                rag_service=...,
                dataset=...
            )
        """

        # -----------------------------------------------------
        # Mode 1: Direct evaluation
        # -----------------------------------------------------

        if (
            question is not None
            and answer is not None
            and reference_answer is not None
            and context is not None
        ):
            return {
                "answer_overlap": answer_keyword_overlap(
                    answer,
                    reference_answer,
                ),
                "faithfulness": faithfulness_score(
                    answer,
                    context,
                ),
                "answer_relevance": answer_relevance_score(
                    question,
                    answer,
                ),
            }

        # -----------------------------------------------------
        # Mode 2: Dataset-based evaluation
        # -----------------------------------------------------

        if rag_service is not None and dataset is not None:

            results = []

            for case in dataset:

                results.append(
                    self.evaluate_case(
                        rag_service,
                        case,
                    )
                )

            if not results:
                return {
                    "cases": [],
                    "metrics": {},
                }

            metric_names = [
                "answer_overlap",
                "answer_relevance",
                "faithfulness_baseline",
            ]

            averages = {}

            for metric in metric_names:

                values = [
                    item["metrics"][metric]
                    for item in results
                ]

                averages[metric] = (
                    sum(values) / len(values)
                )

            return {
                "cases": results,
                "metrics": averages,
            }

        raise ValueError(
            "Invalid evaluation arguments. "
            "Provide question, answer, reference_answer, "
            "and context, or provide rag_service and dataset."
        )

    # ---------------------------------------------------------
    # Dataset case evaluation
    # ---------------------------------------------------------

    def evaluate_case(
        self,
        rag_service,
        case,
    ):

        result = rag_service.query(
            question=case.question
        )

        answer = result["answer"]
        context = result["context"]

        return {
            "id": case.id,
            "question": case.question,
            "answer": answer,
            "metrics": {
                "answer_overlap": answer_keyword_overlap(
                    answer,
                    case.reference_answer,
                ),
                "answer_relevance": answer_relevance_score(
                    case.question,
                    answer,
                ),
                "faithfulness_baseline": faithfulness_score(
                    answer,
                    context,
                ),
            },
        }