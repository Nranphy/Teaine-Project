from teaine_common.sdk.ruler.auth import build_auth_headers
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
