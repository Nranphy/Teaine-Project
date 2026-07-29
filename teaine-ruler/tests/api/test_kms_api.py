import asyncio

from fastapi.testclient import TestClient
from sqlalchemy import desc, select

from app.app import create_app
from app.infra.postgres.tables import kms_entries
from app.services import get_services

HEADERS = {"X-Teaine-Service": "dev", "X-Teaine-Api-Key": "dev-secret"}


async def _get_latest_stored_value(namespace: str, key: str) -> str:
    async with get_services().postgres_session_factory() as session:
        statement = (
            select(kms_entries.c.value)
            .where(
                kms_entries.c.namespace == namespace,
                kms_entries.c.key == key,
            )
            .order_by(desc(kms_entries.c.version))
            .limit(1)
        )
        stored_value = await session.scalar(statement)
        assert stored_value is not None
        return stored_value


def test_kms_set_and_get():
    client = TestClient(create_app())
    put = client.put(
        "/api/v1/internal/kms/test/example", headers=HEADERS, json={"value": "ok"}
    )
    assert put.status_code == 200
    assert put.json()["version"] == 1

    put = client.put(
        "/api/v1/internal/kms/test/example", headers=HEADERS, json={"value": "new"}
    )
    assert put.status_code == 200
    assert put.json()["version"] == 2
    assert asyncio.run(_get_latest_stored_value("test", "example")) != "new"

    get = client.get("/api/v1/internal/kms/test/example", headers=HEADERS)
    assert get.status_code == 200
    assert get.json()["value"] == "new"
    assert get.json()["version"] == 2
