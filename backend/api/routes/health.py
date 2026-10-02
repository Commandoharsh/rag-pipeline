import sqlite3
import time
from pathlib import Path

from fastapi import APIRouter

from backend.config import settings


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


def check_sqlite():
    """
    Check SQLite database connectivity.
    """

    start = time.perf_counter()

    try:
        database_path = Path("data/researchrag.db")

        database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        connection = sqlite3.connect(
            database_path,
            timeout=2,
        )

        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()

        connection.close()

        latency_ms = (
            time.perf_counter() - start
        ) * 1000

        return {
            "status": "healthy",
            "latency_ms": round(latency_ms, 2),
            "database": str(database_path),
        }

    except Exception as exc:
        return {
            "status": "unhealthy",
            "error": str(exc),
        }


def check_qdrant():
    """
    Check Qdrant connectivity.
    """

    start = time.perf_counter()

    try:
        from qdrant_client import QdrantClient

        client = QdrantClient(
            host="localhost",
            port=6333,
            timeout=2,
        )

        client.get_collections()

        latency_ms = (
            time.perf_counter() - start
        ) * 1000

        return {
            "status": "healthy",
            "latency_ms": round(latency_ms, 2),
        }

    except Exception as exc:
        return {
            "status": "unhealthy",
            "error": str(exc),
        }


def check_embeddings():
    """
    Check whether the embedding model can be loaded.
    """

    start = time.perf_counter()

    try:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        vector = model.encode(
            ["health check"],
            normalize_embeddings=True,
        )

        if vector is None or len(vector) == 0:
            raise RuntimeError(
                "Embedding model returned no vector."
            )

        latency_ms = (
            time.perf_counter() - start
        ) * 1000

        return {
            "status": "healthy",
            "model": "all-MiniLM-L6-v2",
            "dimension": len(vector[0]),
            "latency_ms": round(latency_ms, 2),
        }

    except Exception as exc:
        return {
            "status": "unhealthy",
            "error": str(exc),
        }


def check_ollama():
    """
    Check Ollama availability.
    """

    start = time.perf_counter()

    try:
        import requests

        response = requests.get(
            f"{settings.OLLAMA_BASE_URL}/api/tags",
            timeout=3,
        )

        response.raise_for_status()

        data = response.json()

        models = [
            model.get("name")
            for model in data.get("models", [])
        ]

        latency_ms = (
            time.perf_counter() - start
        ) * 1000

        model_configured = (
            settings.OLLAMA_MODEL in models
            or f"{settings.OLLAMA_MODEL}:latest" in models
        )

        return {
            "status": "healthy",
            "base_url": settings.OLLAMA_BASE_URL,
            "configured_model": settings.OLLAMA_MODEL,
            "model_available": model_configured,
            "models": models,
            "latency_ms": round(latency_ms, 2),
        }

    except Exception as exc:
        return {
            "status": "unhealthy",
            "base_url": settings.OLLAMA_BASE_URL,
            "error": str(exc),
        }


@router.get("")
def health_check():
    """
    Detailed ResearchRAG health check.
    """

    services = {
        "sqlite": check_sqlite(),
        "qdrant": check_qdrant(),
        "embeddings": check_embeddings(),
        "ollama": check_ollama(),
    }

    unhealthy_services = [
        name
        for name, result in services.items()
        if result["status"] != "healthy"
    ]

    overall_status = (
        "healthy"
        if not unhealthy_services
        else "degraded"
    )

    return {
        "status": overall_status,
        "service": "ResearchRAG",
        "services": services,
        "unhealthy_services": unhealthy_services,
    }