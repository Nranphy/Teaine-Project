from teaine_common.models.base import TeaineModel


class KmsKey(TeaineModel):
    namespace: str
    key: str


class KmsEntry(KmsKey):
    value: str
    version: int


class KmsEntryUpdate(TeaineModel):
    value: str


__all__ = ["KmsEntry", "KmsEntryUpdate", "KmsKey"]
