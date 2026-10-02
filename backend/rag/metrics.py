from dataclasses import dataclass


@dataclass
class RAGMetrics:

    preprocessing_ms: float = 0
    rewriting_ms: float = 0
    retrieval_ms: float = 0
    fusion_ms: float = 0
    compression_ms: float = 0
    generation_ms: float = 0
    total_ms: float = 0

    retrieved_documents: int = 0
    final_documents: int = 0