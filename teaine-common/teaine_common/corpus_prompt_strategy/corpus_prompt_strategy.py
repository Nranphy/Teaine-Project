from abc import ABC, abstractmethod

from ..models.corpus import Corpus, KNOWLEDGE_KEYS


class CorpusPromptStrategy(ABC):
    """统一语料 Corpus 转 Prompt 文本策略抽象类"""

    last_n_knowledge: int
    """要求有知识的最后的消息数量，用于 Corpus 对象构建参考"""

    knowledge_keys: tuple[KNOWLEDGE_KEYS]
    """需要使用的知识文本块，用于 Corpus 对象构建参考"""

    @classmethod
    def check(cls, corpus: Corpus) -> bool:
        """检查语料是否满足策略要求"""
        keys_ls = []
        for i, msg in enumerate(corpus.data[::]):
            if i < cls.last_n_knowledge:
                if not msg.knowledge:
                    return False
            keys_ls.extend(msg.knowledge.keys())
        keys_set = set(keys_ls)
        for key in keys_set:
            if key not in cls.knowledge_keys:
                return False
        return True

    @classmethod
    @abstractmethod
    def convert(cls, corpus: Corpus) -> str:
        """Corpus 实例转 Prompt 文本"""
        raise NotImplementedError('Corpus 转 Prompt str 方法未实现。')


__all__ = [
    "CorpusPromptStrategy",
]
