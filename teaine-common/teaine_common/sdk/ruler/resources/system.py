from teaine_common.errors import VersionMismatchError
from teaine_common.models.system import HealthResponse, SystemInfo
from teaine_common.version import __version__


class RulerSystemResource:
    def __init__(self, client):
        self._client = client

    async def health(self) -> HealthResponse:
        data = await self._client.request("GET", "/api/v1/public/health", auth=False)
        return HealthResponse.model_validate(data)

    async def info(self) -> SystemInfo:
        data = await self._client.request("GET", "/api/v1/internal/system/info")
        return SystemInfo.model_validate(data)

    async def ensure_common_version(self) -> None:
        info = await self.info()
        if info.common_version != __version__:
            raise VersionMismatchError(__version__, info.common_version)


__all__ = ["RulerSystemResource"]
