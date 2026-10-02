from backend.rag.generation.citation_extractor import (
    CitationExtractor
)

from backend.rag.generation.citation_validator import (
    CitationValidator
)

from backend.rag.generation.response_builder import (
    ResponseBuilder
)


class CitationService:

    def __init__(self):

        self.extractor = CitationExtractor()
        self.validator = CitationValidator()
        self.builder = ResponseBuilder()

    def build_response(
        self,
        answer: str,
        results
    ):

        citation_ids = (
            self.extractor.extract(
                answer
            )
        )

        valid_ids = (
            self.validator.validate(
                citation_ids,
                len(results)
            )
        )

        return self.builder.build(
            answer=answer,
            results=results,
            citation_ids=valid_ids
        )