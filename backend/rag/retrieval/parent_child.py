from dataclasses import dataclass


@dataclass
class ParentChunk:
    parent_id: str
    content: str
    metadata: dict


class ParentChildRetriever:

    def __init__(self):
        self.parents = {}

    def add_parent(
        self,
        parent_id: str,
        content: str,
        metadata: dict,
    ):
        self.parents[parent_id] = ParentChunk(
            parent_id=parent_id,
            content=content,
            metadata=metadata,
        )

    def get_parent(self, parent_id: str):
        return self.parents.get(parent_id)

    def expand(self, results):

        expanded = []

        for result in results:

            parent_id = result.metadata.get(
                "parent_id"
            )

            if not parent_id:
                expanded.append(result)
                continue

            parent = self.parents.get(parent_id)

            if parent is None:
                expanded.append(result)
                continue

            result.content = parent.content

            expanded.append(result)

        return expanded