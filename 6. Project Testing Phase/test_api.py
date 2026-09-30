from fastapi.testclient import TestClient

from app.main import app


def test_health():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_prompt_validation():
    client = TestClient(app)
    response = client.post("/generate-comic/json", json={"story_prompt":"x"})
    assert response.status_code == 422
