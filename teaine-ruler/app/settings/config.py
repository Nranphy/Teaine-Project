from functools import lru_cache
from pathlib import Path

from pydantic import DirectoryPath, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "ruler"
    data_dir: DirectoryPath = Path(__file__).parents[1] / "data"
    prompt_data_dir: DirectoryPath | None = None
    corpus_data_dir: DirectoryPath | None = None
    kms_data_file: Path | None = None
    database_url: str | None = None
    internal_api_keys: dict[str, str] = Field(
        default_factory=lambda: {"dev": "dev-secret"}
    )

    model_config = SettingsConfigDict(
        env_prefix="TEAINE_RULER_", env_nested_delimiter="__"
    )

    @model_validator(mode="after")
    def prepare_paths(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if self.prompt_data_dir is None:
            self.prompt_data_dir = self.data_dir / "prompt"
        if self.corpus_data_dir is None:
            self.corpus_data_dir = self.data_dir / "corpus"
        if self.kms_data_file is None:
            self.kms_data_file = self.data_dir / "kms.json"
        self.prompt_data_dir.mkdir(parents=True, exist_ok=True)
        self.corpus_data_dir.mkdir(parents=True, exist_ok=True)
        self.kms_data_file.parent.mkdir(parents=True, exist_ok=True)
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()


__all__ = ["Settings", "get_settings"]
