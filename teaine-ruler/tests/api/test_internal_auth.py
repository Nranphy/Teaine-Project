from fastapi.testclient import TestClient

from app.app import create_app
from teaine_common.version import __version__


def test_internal_requires_auth():
    response = TestClient(create_app()).get("/api/v1/internal/system/info")
    assert response.status_code == 401


def test_internal_accepts_dev_key():
    response = TestClient(create_app()).get(
        "/api/v1/internal/system/info",
        headers={"X-Teaine-Service": "dev", "X-Teaine-Api-Key": "dev-secret"},
    )
    assert response.status_code == 200
    assert response.json()["service"] == "ruler"
    assert response.json()["common_version"] == __version__
