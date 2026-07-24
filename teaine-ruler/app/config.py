import os
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


RULER_ROOT = Path(__file__).resolve().parents[1]
ENV_NAME = os.environ.get("TEAINE_RULER_ENV", "test")
ENV_FILES = {
    "test": RULER_ROOT / ".env.test",
    "prod": RULER_ROOT / ".env.prod",
}
ENV_FILE = ENV_FILES.get(ENV_NAME, ENV_FILES["test"])


def load_env_file(path: Path) -> None:
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


load_env_file(ENV_FILE)


class Settings(BaseSettings):
    service_name: str
    database_url: str
    internal_api_keys: dict[str, str]

    model_config = SettingsConfigDict(
        env_ignore_empty=True,
        env_prefix="TEAINE_RULER_",
        env_nested_delimiter="__",
        extra="ignore",
    )

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


def load_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]


settings = load_settings()

__all__ = ["ENV_FILE", "ENV_NAME", "Settings", "load_env_file", "load_settings", "settings"]
