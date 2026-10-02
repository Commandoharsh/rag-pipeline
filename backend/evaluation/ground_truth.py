from dataclasses import dataclass


@dataclass
class GroundTruthCase:
    id: str
    question: str
    relevant_chunks: set[str]
    reference_answer: str