from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api.errors import global_exception_handler
from backend.api.routes.indexing import router as indexing_router
from backend.api.routes.query import router as query_router
from backend.api.routes.stream import router as stream_router
from backend.rag.application import create_rag_application
from fastapi.middleware.cors import CORSMiddleware
from backend.utils.logging_config import configure_logging
from backend.api.error_handler import global_exception_handler
from backend.api.routes.health import router as health_router
from backend.api.request_id import (
    RequestIDMiddleware
)
from backend.api.routes.documents import (
    router as documents_router
)
from backend.api.routes.auth import (
    router as auth_router,
)
from backend.api.routes.conversation_query import (
    router as conversation_query_router
)
from backend.api.timing import (
    TimingMiddleware
)
from backend.api.request_id import RequestIDMiddleware



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_rag_application()
    yield


app = FastAPI(
    title="ResearchRAG",
    description="Intelligent Research & Technical Knowledge Platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_exception_handler(
    Exception,
    global_exception_handler
)

app.include_router(indexing_router)
app.include_router(query_router)
app.include_router(stream_router)
app.include_router(
    documents_router
)
app.include_router(
    auth_router
)
app.include_router(
    conversation_query_router
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    RequestIDMiddleware
)
app.add_middleware(
    TimingMiddleware
)
app.add_exception_handler(
    Exception,
    global_exception_handler,
)

app.include_router(health_router)
app.add_middleware(
    RequestIDMiddleware
)


@app.get("/")
def root():
    return {
        "project": "ResearchRAG",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    try:
        application = create_rag_application()

        chunks = application.state.vector_store.get_all_chunks()

        return {
            "status": "healthy",
            "vector_store": "available",
            "indexed_chunks": len(chunks),
            "llm_provider": "ollama",
            "llm_model": application.llm.model,
        }

    except Exception as exc:
        return {
            "status": "degraded",
            "error": str(exc),
        }