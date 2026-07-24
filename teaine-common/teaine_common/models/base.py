from pydantic import BaseModel, ConfigDict, Field

from teaine_common.types import JSONObject, current_timestamp_ms


class TeaineModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class ErrorResponse(TeaineModel):
    code: str
    message: str
    details: JSONObject = Field(default_factory=dict)


class TimestampedModel(TeaineModel):
    created_at: int = Field(default_factory=current_timestamp_ms)


__all__ = ["ErrorResponse", "TeaineModel", "TimestampedModel"]
