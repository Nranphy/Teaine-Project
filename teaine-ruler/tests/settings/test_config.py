import pytest
from pydantic import ValidationError

from config import Settings


REQUIRED_ENV_VARS = [
    "TEAINE_RULER_SERVICE_NAME",
    "TEAINE_RULER_DATA_DIR",
    "TEAINE_RULER_PROMPT_DATA_DIR",
    "TEAINE_RULER_CORPUS_DATA_DIR",
    "TEAINE_RULER_KMS_DATA_FILE",
    "TEAINE_RULER_DATABASE_URL",
    "TEAINE_RULER_INTERNAL_API_KEYS",
]


def test_settings_requires_all_runtime_parameters(monkeypatch):
    for env_var in REQUIRED_ENV_VARS:
        monkeypatch.delenv(env_var, raising=False)

    with pytest.raises(ValidationError) as exc_info:
        Settings()

    missing_fields = {error["loc"][0] for error in exc_info.value.errors()}
    assert missing_fields == {
        "service_name",
        "data_dir",
        "prompt_data_dir",
        "corpus_data_dir",
        "kms_data_file",
        "database_url",
        "internal_api_keys",
    }


def test_settings_rejects_blank_values(monkeypatch, tmp_path):
    monkeypatch.setenv("TEAINE_RULER_SERVICE_NAME", " ")
    monkeypatch.setenv("TEAINE_RULER_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("TEAINE_RULER_PROMPT_DATA_DIR", str(tmp_path / "prompt"))
    monkeypatch.setenv("TEAINE_RULER_CORPUS_DATA_DIR", str(tmp_path / "corpus"))
    monkeypatch.setenv("TEAINE_RULER_KMS_DATA_FILE", str(tmp_path / "kms.json"))
    monkeypatch.setenv("TEAINE_RULER_DATABASE_URL", " ")
    monkeypatch.setenv("TEAINE_RULER_INTERNAL_API_KEYS", '{"dev":""}')

    with pytest.raises(ValidationError):
        Settings()
