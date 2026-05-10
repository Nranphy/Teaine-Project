"""实体模型基础组件"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


def current_timestamp_ms() -> int:
    """返回当前毫秒时间戳"""
    return int(datetime.now().timestamp() * 1000)


class EntityModel(BaseModel):
    """实体模型基类"""

    model_config = ConfigDict(extra='forbid')


__all__ = [
    'EntityModel',
    'current_timestamp_ms',
]
