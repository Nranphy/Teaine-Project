from io import BytesIO
from urllib.error import HTTPError

import pytest

from teaine_common.errors import VersionMismatchError
from teaine_common.sdk.ruler.auth import build_auth_headers
from teaine_common.sdk.ruler import client as ruler_client_module
from teaine_common.sdk.ruler.client import RulerClient
from teaine_common.version import __version__


def test_build_auth_headers():
    headers = build_auth_headers("grail", "secret")
    assert headers["X-Teaine-Service"] == "grail"
    assert headers["X-Teaine-Api-Key"] == "secret"
    assert headers["X-Teaine-Common-Version"] == __version__


def test_ruler_client_exposes_current_resources():
    client = RulerClient("http://localhost:8000", "grail", "secret")
    assert hasattr(client, "system")
    assert hasattr(client, "kms")
    assert hasattr(client, "prompt")
    assert not hasattr(client, "corpus")
    assert not hasattr(client.system, "ensure_common_version")


def test_ruler_client_maps_common_version_mismatch(monkeypatch):
    def raise_http_error(request, timeout):
        body = (
            b'{"client_common_version":"0.0.0",'
            b'"server_common_version":"0.1.0"}'
        )
        raise HTTPError(
            request.full_url,
            426,
            "Upgrade Required",
            hdrs=None,
            fp=BytesIO(body),
        )

    monkeypatch.setattr(ruler_client_module, "urlopen", raise_http_error)

    client = RulerClient("http://localhost:8000", "grail", "secret")
    with pytest.raises(VersionMismatchError) as exc_info:
        client._request_sync(
            "GET",
            "/api/v1/internal/system/info",
            auth=True,
            json=None,
            headers=None,
        )

    assert exc_info.value.local_version == "0.0.0"
    assert exc_info.value.remote_version == "0.1.0"
