from datetime import datetime

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: str
    email: str
    is_active: bool
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class CitationResponse(BaseModel):
    chunk_id: str
    source: str
    page: str


class RAGResponse(BaseModel):
    question: str
    answer: str
    rewritten_query: str | None = None
    queries: list[str] = []
    citations: list[CitationResponse] = []