from teaine_common.models.corpus import CorpusAdd, DatasetInfo


class RulerCorpusResource:
    def __init__(self, client):
        self._client = client

    async def list(self) -> list[DatasetInfo]:
        data = await self._client.request("GET", "/api/v1/internal/corpus")
        return [DatasetInfo.model_validate(item) for item in data]

    async def create(self, dataset: DatasetInfo) -> DatasetInfo:
        data = await self._client.request(
            "POST", "/api/v1/internal/corpus", json=dataset.model_dump()
        )
        return DatasetInfo.model_validate(data)

    async def add(self, payload: CorpusAdd) -> DatasetInfo:
        data = await self._client.request(
            "POST", "/api/v1/internal/corpus/items", json=payload.model_dump()
        )
        return DatasetInfo.model_validate(data)


__all__ = ["RulerCorpusResource"]
