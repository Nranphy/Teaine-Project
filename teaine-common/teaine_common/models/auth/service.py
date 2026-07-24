from pydantic import Field

from teaine_common.models.base import TeaineModel


class ServiceIdentity(TeaineModel):
    name: str
    scopes: list[str] = Field(default_factory=list)


__all__ = ["ServiceIdentity"]
