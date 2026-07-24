from fastapi.testclient import TestClient

from app.app import create_app

HEADERS = {"X-Teaine-Service": "dev", "X-Teaine-Api-Key": "dev-secret"}


def test_prompt_render():
    client = TestClient(create_app())
    create = client.post(
        "/api/v1/internal/prompt",
        headers=HEADERS,
        json={
            "name": "test_prompt",
            "description": "test prompt",
            "content": "hi {{{name}}}",
            "params": "name",
        },
    )
    assert create.status_code == 200

    response = client.post(
        "/api/v1/internal/prompt/test_prompt/render",
        headers=HEADERS,
        json={"params": {"name": "tea"}},
    )
    assert response.status_code == 200
    assert response.json()["text"] == "hi tea"

    missing = client.post(
        "/api/v1/internal/prompt/test_prompt/render",
        headers=HEADERS,
        json={"params": {}},
    )
    assert missing.status_code == 400
