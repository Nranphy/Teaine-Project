from teaine_common.models.tool import HolidayDateInfo


class RulerToolResource:
    def __init__(self, client):
        self._client = client

    async def holiday(self, date: str) -> HolidayDateInfo:
        data = await self._client.request(
            "GET", f"/api/v1/internal/tool/holidays/date/{date}"
        )
        return HolidayDateInfo.model_validate(data)


__all__ = ["RulerToolResource"]

