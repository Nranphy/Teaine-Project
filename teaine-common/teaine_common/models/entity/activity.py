"""业务活动实体模型"""

from pydantic import Field
from typing import Any

from teaine_common.models.enums import ActivityTypeEnum
from .base import EntityModel, current_timestamp_ms


class Activity(EntityModel):
    """一次完整的直播、对话、推文、社区等业务活动"""

    id: int | None = None
    """业务活动主键 ID"""

    type: ActivityTypeEnum
    """业务活动类型"""

    title: str = ''
    """业务活动标题"""

    description: str = ''
    """业务活动描述"""

    start_timestamp: int = Field(default_factory=current_timestamp_ms)
    """业务活动开始时间戳，单位为毫秒"""

    end_timestamp: int | None = None
    """业务活动结束时间戳，单位为毫秒，未结束时为空"""

    fields: dict[str, Any] = Field(default_factory=dict)
    """业务活动扩展字段"""

    created_at: int = Field(default_factory=current_timestamp_ms)
    """记录创建时间戳，单位为毫秒"""


__all__ = [
    'Activity',
]
