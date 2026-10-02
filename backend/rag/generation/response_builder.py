from backend.rag.generation.response import (
    Citation,
    RAGResponse,
)


class ResponseBuilder:

    def build(
        self,
        answer: str,
        results,
        citation_ids: list[int]
    ) -> RAGResponse:

        citations = []

        for citation_id in citation_ids:

            index = citation_id - 1

            if index < 0 or index >= len(results):
                continue

            result = results[index]

            citations.append(
                Citation(
                    source=result.metadata.get(
                        "source",
                        "unknown"
                    ),
                    page=result.metadata.get(
                        "page",
                        "unknown"
                    ),
                    chunk_id=result.chunk_id
                )
            )

        return RAGResponse(
            answer=answer,
            citations=citations
        )