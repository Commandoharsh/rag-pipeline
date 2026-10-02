from rank_bm25 import BM25Okapi

from backend.rag.retrieval.retrieval_result import RetrievalResult


class BM25Retriever:

    def __init__(self):
        self.chunks = []
        self.bm25 = None

    # =========================================================
    # INDEX
    # =========================================================

    def index(self, chunks):
        """
        Build the BM25 index from document chunks.
        """

        self.chunks = list(chunks)

        # No documents to index
        if not self.chunks:
            self.bm25 = None
            return

        tokenized_documents = [
            chunk.content.lower().split()
            for chunk in self.chunks
        ]

        self.bm25 = BM25Okapi(
            tokenized_documents
        )

    # =========================================================
    # RETRIEVE
    # =========================================================

    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ):
        """
        Retrieve the most relevant chunks using BM25.
        """

        # -----------------------------------------------------
        # Validate query
        # -----------------------------------------------------

        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        # -----------------------------------------------------
        # Make sure the index exists
        # -----------------------------------------------------

        if self.bm25 is None:
            raise ValueError(
                "BM25 retriever has not been indexed."
            )

        # -----------------------------------------------------
        # Tokenize query
        # -----------------------------------------------------

        tokenized_query = query.lower().split()

        # -----------------------------------------------------
        # Calculate BM25 scores
        # -----------------------------------------------------

        scores = self.bm25.get_scores(
            tokenized_query
        )

        # -----------------------------------------------------
        # Rank documents
        # -----------------------------------------------------

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        # -----------------------------------------------------
        # Build retrieval results
        # -----------------------------------------------------

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