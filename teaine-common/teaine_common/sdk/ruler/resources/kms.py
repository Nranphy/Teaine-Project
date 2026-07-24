from teaine_common.models.kms import KmsEntry, KmsEntryUpdate


class RulerKmsResource:
    def __init__(self, client):
        self._client = client

    async def get(self, namespace: str, key: str) -> KmsEntry:
        data = await self._client.request(
            "GET", f"/api/v1/internal/kms/{namespace}/{key}"
        )
        return KmsEntry.model_validate(data)

    async def set(self, namespace: str, key: str, value: str) -> KmsEntry:
        payload = KmsEntryUpdate(value=value).model_dump()
        data = await self._client.request(
            "PUT", f"/api/v1/internal/kms/{namespace}/{key}", json=payload
        )
        return KmsEntry.model_validate(data)

__all__ = ["RulerKmsResource"]
