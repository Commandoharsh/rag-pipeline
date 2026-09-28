from rank_bm25 import BM25Okapi

from backend.rag.retrieval.retrieval_result import RetrievalResult


class BM25Retriever:

    def __init__(self):
        self.chunks = []
        self.bm25 = None

    def index(self, chunks):

        self.chunks = chunks

        tokenized_documents = [
            chunk.content.lower().split()
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(tokenized_documents)

    def retrieve(self, query: str, top_k: int = 5):

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if self.bm25 is None:
            raise ValueError("BM25 index has not been initialized.")

        tokenized_query = query.lower().split()

        scores = self.bm25.get_scores(tokenized_query)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        results = []

        for index in ranked_indices:

            chunk = self.chunks[index]

            results.append(
                RetrievalResult(
                    chunk_id=chunk.chunk_id,
                    content=chunk.content,
                    score=float(scores[index]),
                    metadata=chunk.metadata
                )
            )

        return results