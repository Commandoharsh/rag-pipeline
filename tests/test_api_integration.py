from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_root_endpoint():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == "ResearchRAG"


def test_health_endpoint():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert "status" in data


def test_invalid_query():

    response = client.post(
        "/query",
        json={
            "question": ""
        }
    )

    assert response.status_code == 422


def test_missing_question():

    response = client.post(
        "/query",
        json={}
    )

    assert response.status_code == 422


def test_invalid_file_type():

    response = client.post(
        "/index/pdf",
        files={
            "file": (
                "test.txt",
                b"this is not a pdf",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400