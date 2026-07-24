from fastapi.testclient import TestClient

from app.app import create_app

HEADERS = {"X-Teaine-Service": "dev", "X-Teaine-Api-Key": "dev-secret"}


def test_kms_set_and_get():
    client = TestClient(create_app())
    put = client.put(
        "/api/v1/internal/kms/test/example", headers=HEADERS, json={"value": "ok"}
    )
    assert put.status_code == 200
    get = client.get("/api/v1/internal/kms/test/example", headers=HEADERS)
    assert get.status_code == 200
    assert get.json()["value"] == "ok"
