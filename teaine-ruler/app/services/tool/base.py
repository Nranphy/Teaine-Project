from abc import ABC, abstractmethod
from typing import Generic, TypeVar


InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class BaseTool(ABC, Generic[InputT, OutputT]):
    """工具基类。"""

    @abstractmethod
    async def run(self, payload: InputT) -> OutputT:
        """
        执行工具并返回标准化结果。

        :param payload: 工具输入参数。
        :return: 工具执行结果。
        :raises ToolRunError: 工具执行失败。
        """


class ToolRunError(RuntimeError):
    """工具执行失败。"""


__all__ = ["BaseTool", "ToolRunError"]

