from fastapi.testclient import TestClient

from app.app import create_app


def test_public_health():
    response = TestClient(create_app()).get("/api/v1/public/health")
    assert response.status_code == 200
    assert response.json() == {"service": "ruler", "status": "ok"}
