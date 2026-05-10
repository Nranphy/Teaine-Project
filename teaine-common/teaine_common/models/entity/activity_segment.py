"""业务活动阶段实体模型"""

from pydantic import Field
from typing import Any

from teaine_common.models.enums import ActivitySegmentTypeEnum
from .base import EntityModel, current_timestamp_ms


class ActivitySegment(EntityModel):
    """一次业务活动内的阶段"""

    id: int | None = None
    """业务活动阶段主键 ID"""

    type: ActivitySegmentTypeEnum
    """业务活动阶段类型"""

    activity_id: int
    """关联的业务活动 ID"""

    title: str = ''
    """业务活动阶段标题"""

    description: str = ''
    """业务活动阶段描述"""

    start_timestamp: int = Field(default_factory=current_timestamp_ms)
    """业务活动阶段开始时间戳，单位为毫秒"""

    end_timestamp: int | None = None
    """业务活动阶段结束时间戳，单位为毫秒，未结束时为空"""

    fields: dict[str, Any] = Field(default_factory=dict)
    """业务活动阶段扩展字段"""

    created_at: int = Field(default_factory=current_timestamp_ms)
    """记录创建时间戳，单位为毫秒"""


__all__ = [
    'ActivitySegment',
]
