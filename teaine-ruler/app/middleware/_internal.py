INTERNAL_API_PREFIX = "/api/v1/internal"


def is_internal_api_request(path: str) -> bool:
    """
    判断请求路径是否属于内部 API。

    :param path: HTTP 请求路径。
    :return: 属于内部 API 时返回 True，否则返回 False。
    """

    return path.startswith(INTERNAL_API_PREFIX)


__all__ = ["INTERNAL_API_PREFIX", "is_internal_api_request"]
