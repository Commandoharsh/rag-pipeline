from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Chunk:
    content: str
    metadata: Dict[str, str] = field(default_factory=dict)

    @property
    def chunk_id(self) -> str:
        source = self.metadata.get("source", "unknown")
        page = self.metadata.get("page", "unknown")
        index = self.metadata.get("chunk_index", "0")

        return f"{source}_{page}_{index}"