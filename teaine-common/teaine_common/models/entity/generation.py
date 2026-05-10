"""AI 生成内容实体模型"""

from pydantic import Field
from typing import Any

from .base import EntityModel, current_timestamp_ms


class Generation(EntityModel):
    """业务活动阶段中的模型输入和输出"""

    id: int | None = None
    """生成内容记录主键 ID"""

    activity_segment_id: int
    """关联的业务活动阶段 ID"""

    interaction_ids: list[int] = Field(default_factory=list)
    """关联的用户交互行为 ID 列表，非交互触发时为空列表"""

    input_text: str = ''
    """模型本次生成的主要输入文本"""

    output_text: str = ''
    """模型原始输出文本内容"""

    call_time: int = Field(default_factory=current_timestamp_ms)
    """模型调用开始时间戳，单位为毫秒"""

    return_time: int = Field(default_factory=current_timestamp_ms)
    """模型调用返回时间戳，单位为毫秒"""

    fields: dict[str, Any] = Field(default_factory=dict)
    """生成内容扩展字段"""


__all__ = [
    'Generation',
]
