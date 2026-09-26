from typing import List

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams
)

from backend.rag.chunking.chunk import Chunk


class VectorStore:

    def __init__(
        self,
        collection_name: str = "research_documents",
        vector_size: int = 384
    ):

        self.collection_name = collection_name

        self.client = QdrantClient(
            ":memory:"
        )

        self._create_collection(vector_size)

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

    def add_chunks(
        self,
        chunks: List[Chunk],
        embeddings
    ):

        points = []

        for index, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):

            points.append(
                PointStruct(
                    id=index,
                    vector=embedding.tolist(),
                    payload={
                        "content": chunk.content,
                        "metadata": chunk.metadata
                    }
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(
        self,
        query_embedding,
        limit: int = 5
    ):

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding.tolist(),
            limit=limit
        )

        return results.points