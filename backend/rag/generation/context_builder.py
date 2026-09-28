class ContextBuilder:

    def build(self, results) -> str:

        if not results:
            return ""

        sections = []

        for index, result in enumerate(results, start=1):

            metadata = result.metadata

            source = metadata.get(
                "source",
                "unknown"
            )

            page = metadata.get(
                "page",
                "unknown"
            )

            sections.append(
                f"[SOURCE {index}]\n"
                f"Source: {source}\n"
                f"Page: {page}\n"
                f"Chunk ID: {result.chunk_id}\n"
                f"Score: {result.score:.4f}\n\n"
                f"{result.content}"
            )

        return "\n\n---\n\n".join(sections)