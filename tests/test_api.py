from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == "ResearchRAG"
    assert data["status"] == "running"
    assert data["version"] == "1.0.0"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] in ["healthy", "degraded"]


def test_invalid_query():
    response = client.post(
        "/query",
        json={
            "question": ""
        }
    )

    assert response.status_code == 422


def test_query_missing_question():
    response = client.post(
        "/query",
        json={}
    )

    assert response.status_code == 422