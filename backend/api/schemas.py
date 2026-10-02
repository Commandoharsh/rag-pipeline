from pydantic import BaseModel, Field


class QueryRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask ResearchRAG"
    )

    conversation_context: str | None = Field(
        default=None,
        description="Optional conversation context"
    )


class CitationResponse(BaseModel):

    source: str
    page: str
    chunk_id: str


class QueryResponse(BaseModel):

    question: str

    rewritten_query: str

    answer: str

    citations: list[CitationResponse]