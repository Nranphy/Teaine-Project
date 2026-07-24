from pydantic import Field

from teaine_common.models.base import TeaineModel
from teaine_common.types import JSONObject


class KmsKey(TeaineModel):
    namespace: str
    key: str


class KmsEntry(KmsKey):
    value: str
    metadata: JSONObject = Field(default_factory=dict)


class KmsEntryCreate(KmsEntry):
    pass


class KmsEntryUpdate(TeaineModel):
    value: str
    metadata: JSONObject = Field(default_factory=dict)


__all__ = ["KmsEntry", "KmsEntryCreate", "KmsEntryUpdate", "KmsKey"]
