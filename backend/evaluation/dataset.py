from dataclasses import dataclass


@dataclass
class EvaluationCase:
    id: str
    question: str
    relevant_chunks: set[str]
    reference_answer: str


EVALUATION_DATASET = [
    EvaluationCase(
        id="rag_001",
        question="What is retrieval augmented generation?",
        relevant_chunks={"rag.pdf_1_0"},
        reference_answer=(
            "Retrieval augmented generation combines information "
            "retrieval with language generation so that a language "
            "model can answer using retrieved external context."
        ),
    ),
    EvaluationCase(
        id="ml_001",
        question="How does machine learning help healthcare?",
        relevant_chunks={"healthcare.pdf_2_0"},
        reference_answer=(
            "Machine learning can analyze healthcare data to support "
            "prediction, classification, diagnosis, and decision-making."
        ),
    ),
    EvaluationCase(
        id="transformer_001",
        question="What is transformer attention?",
        relevant_chunks={"transformers.pdf_5_1"},
        reference_answer=(
            "Transformer attention allows a model to determine which "
            "parts of an input sequence are most relevant to each other."
        ),
    ),
]