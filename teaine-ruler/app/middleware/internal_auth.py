"""
内部服务鉴权中间件。

该中间件只拦截 /api/v1/internal 下的接口，公开接口不受影响。
鉴权通过后，会把服务身份写入 request.state.service_identity。
"""

from collections.abc import Awaitable, Callable

from fastapi import Request, Response, status
from teaine_common.enums.auth import X_TEAINE_API_KEY, X_TEAINE_SERVICE
from teaine_common.models.auth import ServiceIdentity

from app.config import settings


INTERNAL_API_PREFIX = "/api/v1/internal"


async def internal_auth_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """
    校验内部接口请求的服务名和 API key。

    非内部接口会直接放行。内部接口需要携带 X-Teaine-Service 和
    X-Teaine-Api-Key，请求头中的值会与 settings.internal_api_keys
    进行比对。

    :param request: 当前 HTTP 请求。
    :param call_next: FastAPI/Starlette 提供的下一个中间件或路由处理器。
    :return: 鉴权失败时返回 401/403 响应，鉴权通过时返回后续处理结果。
    """

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
