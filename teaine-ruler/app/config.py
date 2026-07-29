import os
from pathlib import Path
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILES: dict[str, str] = {
    'test': '.env.test',
    'prod': '.env.prod',
}


def get_env_file_path(env_name: str) -> Path:
    """:return: 指定环境对应的 env 文件路径。"""
    ruler_root = Path(__file__).resolve().parent.parent
    env_file_name = ENV_FILES.get(env_name, ENV_FILES['test'])
    return ruler_root / env_file_name


class Settings(BaseSettings):
    """全局配置类"""

    service_name: str
    """服务名称，用于内部请求的服务身份标识"""

    database_url: str
    """数据库连接地址，用于初始化 Ruler 数据库访问"""

    internal_api_keys: dict[str, str]
    """内部服务 API key 映射，键为服务名称，值为对应密钥"""

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
    """加载 env 文件返回运行配置实例"""
    env_name = os.environ.get('TEAINE_RULER_ENV', 'test')
    env_file = get_env_file_path(env_name)
    if not env_file.exists():
        raise FileNotFoundError(f'Env file not found: {env_file}')
    return Settings(_env_file=env_file)  # pyright: ignore[reportCallIssue]


settings = load_settings()

__all__ = [
    'Settings',
    'settings',
]
