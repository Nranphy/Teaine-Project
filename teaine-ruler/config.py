from pathlib import Path
from typing import Any, Self

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


RULER_ROOT = Path(__file__).resolve().parent
ENV_FILE = RULER_ROOT / ".env"


class Settings(BaseSettings):
    service_name: str
    data_dir: Path
    prompt_data_dir: Path
    corpus_data_dir: Path
    kms_data_file: Path
    database_url: str
    internal_api_keys: dict[str, str]

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        env_prefix="TEAINE_RULER_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    @field_validator(
        "data_dir",
        "prompt_data_dir",
        "corpus_data_dir",
        "kms_data_file",
        mode="before",
    )
    @classmethod
    def reject_blank_path(cls, value: Any) -> Any:
        if isinstance(value, str) and not value.strip():
            raise ValueError("must not be blank")
        return value

    @field_validator("service_name", "database_url")
    @classmethod
    def reject_blank_string(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be blank")
        return value

    @field_validator("internal_api_keys")
    @classmethod
    def reject_empty_api_keys(cls, value: dict[str, str]) -> dict[str, str]:
        if not value:
            raise ValueError("must not be empty")
        for service_name, api_key in value.items():
            if not service_name.strip() or not api_key.strip():
                raise ValueError("service names and api keys must not be blank")
        return value

    @model_validator(mode="after")
    def prepare_paths(self) -> Self:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.prompt_data_dir.mkdir(parents=True, exist_ok=True)
        self.corpus_data_dir.mkdir(parents=True, exist_ok=True)
        self.kms_data_file.parent.mkdir(parents=True, exist_ok=True)
        return self


def load_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]


settings = load_settings()

__all__ = ["Settings", "load_settings", "settings"]
