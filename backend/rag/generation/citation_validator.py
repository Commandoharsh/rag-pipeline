class CitationValidator:

    def validate(
        self,
        citation_ids: list[int],
        source_count: int
    ) -> list[int]:

        valid = []

        for citation_id in citation_ids:

            if 1 <= citation_id <= source_count:
                valid.append(citation_id)

        return sorted(set(valid))