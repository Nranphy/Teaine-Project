from functools import lru_cache

from app.infra.postgres.engine import (
    create_postgres_engine,
    create_session_factory,
)
from app.services.kms import KmsService
from app.services.prompt import PromptService
from app.services.system import SystemService
from app.config import settings


class Services:
    """
    应用服务容器。

    负责创建共享基础设施对象，并把各个业务服务装配在一起。
    模块级的 get_services() 缓存会让该容器成为进程内单例，
    从而在请求之间复用数据库 engine、session factory 和服务实例。
    """

    def __init__(self):
        """
        初始化服务容器并装配所有服务实例。

        :return: None。
        """

        self.postgres_engine = create_postgres_engine(settings.database_url)
        self.postgres_session_factory = create_session_factory(self.postgres_engine)
        self.kms = KmsService(self.postgres_engine, self.postgres_session_factory)
        self.system = SystemService(self.kms)
        self.prompt = PromptService(
            self.postgres_engine,
            self.postgres_session_factory,
        )


@lru_cache
def get_services() -> Services:
    """
    返回懒加载创建的进程内服务容器。

    :return: 进程内复用的服务容器实例。
    """

    return Services()


__all__ = ["Services", "get_services"]
