from pydantic import Field

from .base import TeaineModel


class PageRequest(TeaineModel):
    limit: int = Field(default=50, ge=1, le=500)
    offset: int = Field(default=0, ge=0)


class PageResponse(TeaineModel):
    total: int
    limit: int
    offset: int


__all__ = ["PageRequest", "PageResponse"]
