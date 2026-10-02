from dataclasses import dataclass, field


@dataclass
class Citation:
    source: str
    page: str
    chunk_id: str


@dataclass
class RAGResponse:
    answer: str
    citations: list[Citation] = field(default_factory=list)