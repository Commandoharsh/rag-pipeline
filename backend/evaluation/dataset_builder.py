from backend.evaluation.ground_truth import GroundTruthCase


class EvaluationDatasetBuilder:

    def __init__(self, vector_store):
        self.vector_store = vector_store

    def get_available_chunks(self):
        return self.vector_store.get_all_chunks()

    def build_case(
        self,
        case_id: str,
        question: str,
        chunk_ids: set[str],
        reference_answer: str,
    ):
        available_chunks = {
            chunk.chunk_id
            for chunk in self.get_available_chunks()
        }

        missing = chunk_ids - available_chunks

        if missing:
            raise ValueError(
                f"Unknown chunk IDs: {sorted(missing)}"
            )

        return GroundTruthCase(
            id=case_id,
            question=question,
            relevant_chunks=chunk_ids,
            reference_answer=reference_answer,
        )