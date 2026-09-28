import math


def recall_at_k(
    retrieved_ids: list[str],
    relevant_ids: set[str],
    k: int
) -> float:
    if not relevant_ids:
        return 0.0

    retrieved = set(retrieved_ids[:k])
    relevant_retrieved = retrieved.intersection(relevant_ids)

    return len(relevant_retrieved) / len(relevant_ids)


def reciprocal_rank(
    retrieved_ids: list[str],
    relevant_ids: set[str]
) -> float:
    for rank, chunk_id in enumerate(retrieved_ids, start=1):
        if chunk_id in relevant_ids:
            return 1.0 / rank

    return 0.0


def mean_reciprocal_rank(
    all_retrieved: list[list[str]],
    all_relevant: list[set[str]]
) -> float:

    if not all_retrieved:
        return 0.0

    scores = [
        reciprocal_rank(retrieved, relevant)
        for retrieved, relevant
        in zip(all_retrieved, all_relevant)
    ]

    return sum(scores) / len(scores)


def ndcg_at_k(
    retrieved_ids: list[str],
    relevant_ids: set[str],
    k: int
) -> float:

    retrieved = retrieved_ids[:k]

    dcg = 0.0

    for rank, chunk_id in enumerate(retrieved, start=1):

        if chunk_id in relevant_ids:
            dcg += 1.0 / math.log2(rank + 1)

    ideal_relevant_count = min(len(relevant_ids), k)

    if ideal_relevant_count == 0:
        return 0.0

    idcg = sum(
        1.0 / math.log2(rank + 1)
        for rank in range(1, ideal_relevant_count + 1)
    )

    return dcg / idcg