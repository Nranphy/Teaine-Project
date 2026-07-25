"""
Common 版本检查中间件。

该中间件负责校验内部请求携带的 teaine-common 版本。
"""

from collections.abc import Awaitable, Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from teaine_common.enums.auth import X_TEAINE_COMMON_VERSION
from teaine_common.version import __version__

from app.middleware._internal import is_internal_api_request


async def common_version_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """
    校验调用方 common 版本是否与服务端一致。

    非内部接口会直接放行。内部接口如果没有携带 X-Teaine-Common-Version，
    会跳过版本检查；如果携带该请求头，则必须与服务端导入的 common 版本一致。

    :param request: 当前 HTTP 请求。
    :param call_next: FastAPI/Starlette 提供的下一个中间件或路由处理器。
    :return: 版本不一致时返回 426 响应，否则返回后续处理结果。
    """

    if not is_internal_api_request(request.url.path):
        return await call_next(request)

    common_version = request.headers.get(X_TEAINE_COMMON_VERSION)
    if common_version is not None and common_version != __version__:
        return JSONResponse(
            {
                "detail": "common version mismatch",
                "client_common_version": common_version,
                "server_common_version": __version__,
            },
            status_code=status.HTTP_426_UPGRADE_REQUIRED,
        )

    return await call_next(request)


__all__ = ["common_version_middleware"]
