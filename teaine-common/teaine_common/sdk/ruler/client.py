import asyncio
import json as jsonlib
from collections.abc import Mapping
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from teaine_common.errors import AuthenticationError, RulerAPIError
from teaine_common.sdk.ruler.auth import build_auth_headers
from teaine_common.sdk.ruler.config import RulerClientConfig
from teaine_common.sdk.ruler.resources import (
    RulerKmsResource,
    RulerPromptResource,
    RulerSystemResource,
)


class RulerClient:
    def __init__(
        self, base_url: str, service_name: str, api_key: str, timeout: float = 10.0
    ):
        self.config = RulerClientConfig(
            base_url=base_url,
            service_name=service_name,
            api_key=api_key,
            timeout=timeout,
        )
        self.base_url = str(self.config.base_url).rstrip("/")
        self.system = RulerSystemResource(self)
        self.kms = RulerKmsResource(self)
        self.prompt = RulerPromptResource(self)

    async def aclose(self) -> None:
        return None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

    async def request(
        self,
        method: str,
        path: str,
        *,
        auth: bool = True,
        json: Any = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        return await asyncio.to_thread(
            self._request_sync,
            method,
            path,
            auth=auth,
            json=json,
            headers=headers,
        )

    def _request_sync(
        self,
        method: str,
        path: str,
        *,
        auth: bool,
        json: Any,
        headers: Mapping[str, str] | None,
    ) -> Any:
        request_headers = dict(headers or {})
        if auth:
            request_headers.update(
                build_auth_headers(self.config.service_name, self.config.api_key)
            )
        data = None
        if json is not None:
            data = jsonlib.dumps(json).encode("utf-8")
            request_headers.setdefault("Content-Type", "application/json")
        request = Request(
            f"{self.base_url}{path}",
            data=data,
            headers=request_headers,
            method=method,
        )
        try:
            with urlopen(request, timeout=self.config.timeout) as response:
                body = response.read().decode("utf-8")
                return jsonlib.loads(body) if body else None
        except HTTPError as exc:
            body = exc.read().decode("utf-8")
            if exc.code in {401, 403}:
                raise AuthenticationError(exc.code, body) from exc
            raise RulerAPIError(exc.code, body) from exc


__all__ = ["RulerClient"]
