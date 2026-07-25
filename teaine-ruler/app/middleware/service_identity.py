"""
内部服务身份中间件。

该中间件负责读取内部请求中的服务名，并写入 request.state.service_identity。
"""

from collections.abc import Awaitable, Callable

from fastapi import Request, Response, status
from teaine_common.enums.auth import X_TEAINE_SERVICE
from teaine_common.models.auth import ServiceIdentity

from app.middleware._internal import is_internal_api_request


async def service_identity_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """
    解析内部接口调用方的服务身份。

    非内部接口会直接放行。内部接口必须携带 X-Teaine-Service，
    解析成功后会将服务身份写入 request.state.service_identity。

    :param request: 当前 HTTP 请求。
    :param call_next: FastAPI/Starlette 提供的下一个中间件或路由处理器。
    :return: 缺少服务名时返回 401 响应，否则返回后续处理结果。
    """

    if not is_internal_api_request(request.url.path):
        return await call_next(request)

    service_name = request.headers.get(X_TEAINE_SERVICE)
    if not service_name:
        return Response(
            "missing internal service credentials",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    request.state.service_identity = ServiceIdentity(name=service_name)
    return await call_next(request)


__all__ = ["service_identity_middleware"]
