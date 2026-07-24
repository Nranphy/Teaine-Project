from functools import lru_cache

from app.core.corpus import CorpusService
from app.core.kms import KmsService
from app.core.prompt import PromptService
from app.core.system import SystemService
from config import settings


class Services:
    def __init__(self):
        self.kms = KmsService(settings.kms_data_file)
        self.system = SystemService(self.kms)
        self.prompt = PromptService(settings.prompt_data_dir)
        self.corpus = CorpusService(settings.corpus_data_dir)


@lru_cache
def get_services() -> Services:
    return Services()


__all__ = ["Services", "get_services"]
