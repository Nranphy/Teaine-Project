from teaine_common.enums.auth import (
    X_TEAINE_API_KEY,
    X_TEAINE_COMMON_VERSION,
    X_TEAINE_SERVICE,
)
from teaine_common.version import __version__


def build_auth_headers(service_name: str, api_key: str) -> dict[str, str]:
    return {
        X_TEAINE_SERVICE: service_name,
        X_TEAINE_API_KEY: api_key,
        X_TEAINE_COMMON_VERSION: __version__,
    }


__all__ = ["build_auth_headers"]
