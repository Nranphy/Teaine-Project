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
    def __init__(self):
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
    return Services()


__all__ = ["Services", "get_services"]
