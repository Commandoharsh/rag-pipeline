from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.error_handler import global_exception_handler
from backend.api.request_id import RequestIDMiddleware
from backend.api.timing import TimingMiddleware

from backend.api.routes.auth import router as auth_router
from backend.api.routes.conversations import router as conversations_router
from backend.api.routes.conversation_query import (
    router as conversation_query_router,
)
from backend.api.routes.documents import router as documents_router
from backend.api.routes.health import router as health_router
from backend.api.routes.indexing import router as indexing_router
from backend.api.routes.query import router as query_router
from backend.api.routes.stream import router as stream_router

from backend.rag.application import create_rag_application


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


# ============================================================
# CORS
# ============================================================

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


# ============================================================
# Middleware
# ============================================================

app.add_middleware(RequestIDMiddleware)
app.add_middleware(TimingMiddleware)


# ============================================================
# Exception handling
# ============================================================

app.add_exception_handler(
    Exception,
    global_exception_handler,
)


# ============================================================
# API Routers
# ============================================================

app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(indexing_router)
app.include_router(query_router)
app.include_router(stream_router)
app.include_router(conversations_router)
app.include_router(conversation_query_router)
app.include_router(health_router)


# ============================================================
# Root
# ============================================================

@app.get("/")
def root():
    return {
        "project": "ResearchRAG",
        "status": "running",
        "version": "1.0.0",
    }