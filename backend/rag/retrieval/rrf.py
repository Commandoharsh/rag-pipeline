from collections import defaultdict

from backend.rag.retrieval.retrieval_result import RetrievalResult


def reciprocal_rank_fusion(
    result_lists,
    k: int = 60,
    top_k: int = 5
):

    scores = defaultdict(float)
    results_by_id = {}

    for results in result_lists:

        for rank, result in enumerate(results, start=1):

            scores[result.chunk_id] += 1 / (k + rank)

            results_by_id[result.chunk_id] = result

    ranked_ids = sorted(
        scores,
        key=scores.get,
        reverse=True
    )

    fused_results = []

    for chunk_id in ranked_ids[:top_k]:

        original = results_by_id[chunk_id]

        fused_results.append(
            RetrievalResult(
                chunk_id=chunk_id,
                content=original.content,
                score=scores[chunk_id],
                metadata=original.metadata
            )
        )

    return fused_results