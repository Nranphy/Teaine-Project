"""
内部 API key 中间件。

该中间件负责校验内部请求携带的服务 API key。
"""

from collections.abc import Awaitable, Callable

from fastapi import Request, Response, status
from teaine_common.enums.auth import X_TEAINE_API_KEY

from app.config import settings
from app.middleware._internal import is_internal_api_request


async def internal_api_key_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """
    校验内部接口调用方的 API key。

    非内部接口会直接放行。内部接口必须先由服务身份中间件写入
    request.state.service_identity，再使用该服务名查询配置中的 API key。

    :param request: 当前 HTTP 请求。
    :param call_next: FastAPI/Starlette 提供的下一个中间件或路由处理器。
    :return: 缺少 API key 时返回 401，API key 不匹配时返回 403。
    :raises AttributeError: 中间件挂载顺序错误且缺少 service_identity 时抛出。
    """

    if not is_internal_api_request(request.url.path):
        return await call_next(request)

    api_key = request.headers.get(X_TEAINE_API_KEY)
    if not api_key:
        return Response(
            "missing internal service credentials",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    service_name = request.state.service_identity.name
    expected = settings.internal_api_keys.get(service_name)
    if expected is None or expected != api_key:
        return Response(
            "invalid internal service credentials",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return await call_next(request)


__all__ = ["internal_api_key_middleware"]
