from teaine_common.models.system import SystemInfo

from app.services.kms import KmsService


class SystemService:
    """
    系统级服务，用于提供运行时元信息和兼容性检查数据。
    """

    def __init__(self, kms: KmsService):
        """
        初始化系统服务。

        :param kms: 用于读取系统配置和版本信息的 KMS 服务。
        :return: None。
        """

        self.kms = kms

    async def info(self) -> SystemInfo:
        """
        返回 Ruler 服务元信息，包括已存储的 common 版本。

        :return: Ruler 服务信息和 common 版本信息。
        """

        try:
            common_version = (await self.kms.get("system", "common_version")).value
        except KeyError:
            common_version = None
        return SystemInfo(service="ruler", common_version=common_version)


__all__ = ["SystemService"]
