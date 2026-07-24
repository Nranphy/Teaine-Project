from teaine_common.models.system import SystemInfo

from app.core.kms import KmsService


class SystemService:
    def __init__(self, kms: KmsService):
        self.kms = kms

    def info(self) -> SystemInfo:
        try:
            common_version = self.kms.get("system", "common_version").value
        except KeyError:
            common_version = None
        return SystemInfo(service="ruler", common_version=common_version)


__all__ = ["SystemService"]
