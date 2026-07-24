from pydantic import Field

from teaine_common.models.base import TeaineModel
from teaine_common.types import JSONObject


class HealthResponse(TeaineModel):
    service: str
    status: str = "ok"


class SystemInfo(HealthResponse):
    common_version: str | None = None
    details: JSONObject = Field(default_factory=dict)


__all__ = ["HealthResponse", "SystemInfo"]
