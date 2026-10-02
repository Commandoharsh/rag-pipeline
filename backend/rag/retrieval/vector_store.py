from pathlib import Path
from typing import List
from uuid import NAMESPACE_URL, uuid5


from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from backend.rag.chunking.chunk import Chunk


class VectorStore:

    def __init__(
        self,
        collection_name: str = "research_documents",
        vector_size: int = 384,
        storage_path: str = "data/qdrant"
    ):
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.storage_path = storage_path

        Path(storage_path).mkdir(
            parents=True,
            exist_ok=True
        )

        self.client = QdrantClient(
            path=storage_path
        )

        self._create_collection(
            vector_size
        )

    def _create_collection(
        self,
        vector_size: int
    ):
        collections = self.client.get_collections()

        existing_collections = [
            collection.name
            for collection in collections.collections
        ]

        if self.collection_name not in existing_collections:

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )

    def _point_id(
        self,
        chunk: Chunk
    ) -> str:

        return str(
            uuid5(
                NAMESPACE_URL,
                chunk.chunk_id
            )
        )

    def _convert_vector(self, embedding):
        """
        Convert an embedding into a regular Python list.

        Supports:
        - NumPy arrays
        - Python lists
        - Tuples
        """

        if hasattr(embedding, "tolist"):
            return embedding.tolist()

        return list(embedding)

    def add_chunks(
        self,
        chunks: List[Chunk],
        embeddings
    ):

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks must match "
                "number of embeddings."
            )

        points = []

        for chunk, embedding in zip(
            chunks,
            embeddings
        ):

            vector = self._convert_vector(
                embedding
            )

            points.append(
                PointStruct(
                    id=self._point_id(chunk),
                    vector=vector,
                    payload={
                        "content": chunk.content,
                        "metadata": chunk.metadata
                    }
                )
            )

        if not points:
            return

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(
        self,
        query_embedding,
        limit: int = 5
    ):

        if limit <= 0:
            return []

        vector = self._convert_vector(
            query_embedding
        )

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=limit
        )

        return results.points

    def get_all_chunks(self):

        records, _ = self.client.scroll(
            collection_name=self.collection_name,
            limit=10000,
            with_payload=True,
            with_vectors=False
        )

        chunks = []

        for record in records:

            payload = record.payload or {}

            metadata = payload.get(
                "metadata",
                {}
            )

            chunks.append(
                Chunk(
                    content=payload.get(
                        "content",
                        ""
                    ),
                    metadata=metadata
                )
            )

        return chunks

    def close(self):
        """
        Close the Qdrant client.
        """

        if self.client is not None:

            self.client.close()

            self.client = None
    def delete_by_metadata(
    self,
    key: str,
    value: str,
):
       self.client.delete(
        collection_name=self.collection_name,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key=f"metadata.{key}",
                    match=MatchValue(
                        value=value
                    ),
                )
            ]
        ),
    )