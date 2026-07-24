from pathlib import Path

from fastapi.testclient import TestClient

from app.app import create_app

HEADERS = {"X-Teaine-Service": "dev", "X-Teaine-Api-Key": "dev-secret"}


def test_prompt_render():
    Path("app/data/prompt/test_prompt.txt").write_text(
        "hi {{{name}}}", encoding="utf-8-sig"
    )
    response = TestClient(create_app()).post(
        "/api/v1/internal/prompt/test_prompt/render",
        headers=HEADERS,
        json={"params": {"name": "tea"}},
    )
    assert response.status_code == 200
    assert response.json()["text"] == "hi tea"
