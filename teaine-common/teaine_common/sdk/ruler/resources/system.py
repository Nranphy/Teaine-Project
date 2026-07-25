from teaine_common.models.system import HealthResponse, SystemInfo


class RulerSystemResource:
    def __init__(self, client):
        self._client = client

    async def health(self) -> HealthResponse:
        data = await self._client.request("GET", "/api/v1/public/health", auth=False)
        return HealthResponse.model_validate(data)

    async def info(self) -> SystemInfo:
        data = await self._client.request("GET", "/api/v1/internal/system/info")
        return SystemInfo.model_validate(data)

__all__ = ["RulerSystemResource"]
