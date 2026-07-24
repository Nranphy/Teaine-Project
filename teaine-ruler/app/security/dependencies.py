from fastapi import Header, HTTPException, status
from teaine_common.enums.auth import X_TEAINE_API_KEY, X_TEAINE_SERVICE
from teaine_common.models.auth import ServiceIdentity

from app.settings.config import get_settings


async def require_internal_service(
    service_name: str | None = Header(default=None, alias=X_TEAINE_SERVICE),
    api_key: str | None = Header(default=None, alias=X_TEAINE_API_KEY),
) -> ServiceIdentity:
    if not service_name or not api_key:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "missing internal service credentials"
        )
    expected = get_settings().internal_api_keys.get(service_name)
    if expected is None or expected != api_key:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "invalid internal service credentials"
        )
    return ServiceIdentity(name=service_name)


__all__ = ["require_internal_service"]
