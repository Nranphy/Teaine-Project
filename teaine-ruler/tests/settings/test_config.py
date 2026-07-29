import pytest
from pydantic import ValidationError

from app.config import Settings


REQUIRED_ENV_VARS = [
    "TEAINE_RULER_SERVICE_NAME",
    "TEAINE_RULER_DATABASE_URL",
    "TEAINE_RULER_INTERNAL_API_KEYS",
    "TEAINE_RULER_KMS_SALT",
]


def test_settings_requires_all_runtime_parameters(monkeypatch):
    for env_var in REQUIRED_ENV_VARS:
        monkeypatch.delenv(env_var, raising=False)

    with pytest.raises(ValidationError) as exc_info:
        Settings()

    missing_fields = {error["loc"][0] for error in exc_info.value.errors()}
    assert missing_fields == {
        "service_name",
        "database_url",
        "internal_api_keys",
        "kms_salt",
    }


def test_settings_rejects_blank_values(monkeypatch, tmp_path):
    monkeypatch.setenv("TEAINE_RULER_SERVICE_NAME", " ")
    monkeypatch.setenv("TEAINE_RULER_DATABASE_URL", " ")
    monkeypatch.setenv("TEAINE_RULER_INTERNAL_API_KEYS", '{"dev":""}')
    monkeypatch.setenv("TEAINE_RULER_KMS_SALT", " ")

    with pytest.raises(ValidationError):
        Settings()
