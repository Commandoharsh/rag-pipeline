import re


class CitationExtractor:

    CITATION_PATTERN = re.compile(
        r"\[SOURCE\s+(\d+)\]",
        re.IGNORECASE
    )

    def extract(
        self,
        answer: str
    ) -> list[int]:

        matches = self.CITATION_PATTERN.findall(answer)

        return sorted(
            set(int(match) for match in matches)
        )