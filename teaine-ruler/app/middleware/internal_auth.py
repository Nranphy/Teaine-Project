from collections.abc import Awaitable, Callable

from fastapi import Request, Response, status
from teaine_common.enums.auth import X_TEAINE_API_KEY, X_TEAINE_SERVICE
from teaine_common.models.auth import ServiceIdentity

from app.config import settings


INTERNAL_API_PREFIX = "/api/v1/internal"


async def internal_auth_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    if not request.url.path.startswith(INTERNAL_API_PREFIX):
        return await call_next(request)

    service_name = request.headers.get(X_TEAINE_SERVICE)
    api_key = request.headers.get(X_TEAINE_API_KEY)
    if not service_name or not api_key:
        return Response(
            "missing internal service credentials",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    expected = settings.internal_api_keys.get(service_name)
    if expected is None or expected != api_key:
        return Response(
            "invalid internal service credentials",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    request.state.service_identity = ServiceIdentity(name=service_name)
    return await call_next(request)


__all__ = ["internal_auth_middleware"]
