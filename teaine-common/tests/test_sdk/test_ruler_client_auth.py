from teaine_common.sdk.ruler.auth import build_auth_headers
from teaine_common.version import __version__


def test_build_auth_headers():
    headers = build_auth_headers("grail", "secret")
    assert headers["X-Teaine-Service"] == "grail"
    assert headers["X-Teaine-Api-Key"] == "secret"
    assert headers["X-Teaine-Common-Version"] == __version__
