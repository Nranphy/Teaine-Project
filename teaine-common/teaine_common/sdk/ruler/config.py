from pydantic import AnyHttpUrl, Field

from teaine_common.models.base import TeaineModel


class RulerClientConfig(TeaineModel):
    base_url: AnyHttpUrl
    service_name: str
    api_key: str
    timeout: float = Field(default=10.0, gt=0)


__all__ = ["RulerClientConfig"]
