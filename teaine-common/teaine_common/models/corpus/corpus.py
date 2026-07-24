from typing import Literal

from pydantic import Field, model_validator

from teaine_common.models.base import TeaineModel

ROLE_TYPE = Literal["system", "user", "assistant"]
KNOWLEDGE_KEYS = Literal[
    "user_description", "datetime_info", "background_info", "other"
]


class Role(TeaineModel):
    role_type: ROLE_TYPE
    name: str | None = None

    @model_validator(mode="after")
    def strip_name(self):
        if self.name is not None:
            self.name = self.name.strip()
        return self


class Message(TeaineModel):
    role: Role
    content: str
    knowledge: dict[KNOWLEDGE_KEYS, str] = Field(default_factory=dict)

    @model_validator(mode="after")
    def strip_text(self):
        self.content = self.content.strip()
        self.knowledge = {k: v.strip() for k, v in self.knowledge.items()}
        return self


class Corpus(TeaineModel):
    data: list[Message]
    role_name_map: dict[str, str] = Field(default_factory=dict, exclude=True)

    @model_validator(mode="after")
    def update_role_name_map(self):
        if self.role_name_map:
            return self
        role_pool: dict[str, set[str]] = {}
        for msg in self.data:
            role_pool.setdefault(msg.role.role_type, set())
            if (
                msg.role.name is not None
                and msg.role.name not in role_pool[msg.role.role_type]
            ):
                role_pool[msg.role.role_type].add(msg.role.name)
                self.role_name_map[msg.role.name] = (
                    f"{msg.role.role_type}{len(role_pool[msg.role.role_type])}"
                )
        for role_type, names in role_pool.items():
            if len(names) == 1:
                self.role_name_map[next(iter(names))] = role_type
        return self


class DatasetInfo(TeaineModel):
    name: str = ""
    description: str = ""
    bucket_num: int = 8

    @model_validator(mode="after")
    def check_bucket_num(self):
        if self.bucket_num < 1:
            raise ValueError("数据分桶数量必须大于等于 1。")
        return self


class CorpusAdd(TeaineModel):
    dataset_name: str
    corpus: Corpus


__all__ = [
    "ROLE_TYPE",
    "KNOWLEDGE_KEYS",
    "Corpus",
    "CorpusAdd",
    "DatasetInfo",
    "Message",
    "Role",
]
