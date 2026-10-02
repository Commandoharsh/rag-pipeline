from pathlib import Path
import sys
import json

# Allow running:
# python scripts/evaluate.py
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT)
    )


from backend.rag.application import (
    create_rag_application,
)

from backend.evaluation.dataset import (
    EVALUATION_DATASET,
)

from backend.evaluation.retrieval_evaluator import (
    RetrievalEvaluator,
)

from backend.evaluation.report import (
    EvaluationReport,
)


def print_retrieval_results(
    name,
    result,
):

    metrics = result["metrics"]

    print()
    print("=" * 60)
    print(name.upper())
    print("=" * 60)

    print(
        f"Recall@1 : {metrics['recall@1']:.4f}"
    )

    print(
        f"Recall@3 : {metrics['recall@3']:.4f}"
    )

    print(
        f"Recall@5 : {metrics['recall@5']:.4f}"
    )

    print(
        f"MRR      : {metrics['mrr']:.4f}"
    )

    print(
        f"nDCG@5   : {metrics['ndcg@5']:.4f}"
    )


def main():

    print("=" * 60)
    print("              ResearchRAG Evaluation")
    print("=" * 60)

    print()
    print(
        f"Evaluation cases: {len(EVALUATION_DATASET)}"
    )

    application = create_rag_application()

    evaluator = RetrievalEvaluator()

    strategies = {
    "semantic": application.semantic_retriever,
    "bm25": application.state.bm25_retriever,
    "hybrid": application.hybrid_retriever,
    "hybrid_reranker": application.reranking_pipeline,
                }

    report = {
        "dataset_size": len(
            EVALUATION_DATASET
        ),
        "retrieval": {},
    }

    for name, retriever in strategies.items():

        print(
            f"\nRunning {name}..."
        )

        result = evaluator.evaluate(
            retriever=retriever,
            dataset=EVALUATION_DATASET,
            top_k=5,
        )

        report["retrieval"][name] = result

        print_retrieval_results(
            name,
            result,
        )

    report_writer = EvaluationReport()

    path = report_writer.save(
        report
    )

    print()
    print("=" * 60)
    print(
        f"Report saved to: {path}"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()