from .base import TeaineError


class RulerAPIError(TeaineError):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(message)


class AuthenticationError(RulerAPIError):
    pass


class VersionMismatchError(TeaineError):
    def __init__(self, local_version: str | None, remote_version: str | None):
        self.local_version = local_version
        self.remote_version = remote_version
        super().__init__(
            f"common version mismatch: local={local_version}, remote={remote_version}"
        )


__all__ = ["AuthenticationError", "RulerAPIError", "VersionMismatchError"]
