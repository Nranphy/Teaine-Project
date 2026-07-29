"""
HTTP 中间件。

集中处理内部服务身份、API key 和 Common 版本校验。
"""

from collections.abc import Awaitable, Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from teaine_common.enums.auth import (
    X_TEAINE_API_KEY,
    X_TEAINE_COMMON_VERSION,
    X_TEAINE_SERVICE,
)
from teaine_common.models.auth import ServiceIdentity
from teaine_common.version import __version__

from app.config import settings


def _is_internal_api_request(path: str) -> bool:
    """
    判断请求路径是否属于内部 API。

    :param path: HTTP 请求路径。
    :return: 属于内部 API 时返回 True，否则返回 False。
    """

    return path.startswith('/api/v1/internal')


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

    if not _is_internal_api_request(request.url.path):
        return await call_next(request)

    service_name = request.headers.get(X_TEAINE_SERVICE)
    if not service_name:
        return Response(
            'missing internal service credentials',
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    request.state.service_identity = ServiceIdentity(name=service_name)
    return await call_next(request)


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

    if not _is_internal_api_request(request.url.path):
        return await call_next(request)

    api_key = request.headers.get(X_TEAINE_API_KEY)
    if not api_key:
        return Response(
            'missing internal service credentials',
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    service_name = request.state.service_identity.name
    expected = settings.internal_api_keys.get(service_name)
    if expected is None or expected != api_key:
        return Response(
            'invalid internal service credentials',
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return await call_next(request)


async def common_version_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """
    校验调用方 common 版本是否与服务端一致。

    非内部接口会直接放行。内部接口如果没有携带 X-Teaine-Common-Version，
    会跳过版本检查；如果携带该请求头，则必须与服务端导入的 common 版本一致。

    :param request: 当前 HTTP 请求。
    :param call_next: FastAPI/Starlette 提供的下一个中间件或路由处理器。
    :return: 版本不一致时返回 426 响应，否则返回后续处理结果。
    """

    if not _is_internal_api_request(request.url.path):
        return await call_next(request)

    common_version = request.headers.get(X_TEAINE_COMMON_VERSION)
    if common_version is not None and common_version != __version__:
        return JSONResponse(
            {
                'detail': 'common version mismatch',
                'client_common_version': common_version,
                'server_common_version': __version__,
            },
            status_code=status.HTTP_426_UPGRADE_REQUIRED,
        )

    return await call_next(request)


__all__ = [
    'common_version_middleware',
    'internal_api_key_middleware',
    'service_identity_middleware',
]
