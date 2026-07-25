from teaine_common.models.system import SystemInfo
from teaine_common.version import __version__


class SystemService:
    """
    系统级服务，用于提供运行时元信息和兼容性检查数据。
    """

    def __init__(self):
        """
        初始化系统服务。

        :return: None。
        """

    async def info(self) -> SystemInfo:
        """
        返回 Ruler 服务元信息，包括服务端当前导入的 common 版本。

        :return: Ruler 服务信息和 common 版本信息。
        """

        return SystemInfo(service="ruler", common_version=__version__)


__all__ = ["SystemService"]
