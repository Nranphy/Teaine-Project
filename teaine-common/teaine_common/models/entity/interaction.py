"""用户交互行为实体模型"""

from typing import Any

from pydantic import Field

from teaine_common.enums import InteractionType

from .base import EntityModel, current_timestamp_ms


class Interaction(EntityModel):
    """业务活动中的用户回复、弹幕、礼物等输入"""

    id: int | None = None
    """交互行为记录主键 ID"""

    type: InteractionType
    """交互行为类型"""

    activity_id: int
    """关联的业务活动 ID"""

    user_id: int
    """关联的用户账号系统 ID"""

    text: str = ""
    """交互行为文本内容"""

    amount: int = 0
    """交互行为总金额，单位为分"""

    item_name: str = ""
    """交互相关项目名称，例如礼物名或订阅套餐名"""

    item_num: int = 0
    """交互相关项目数量，例如礼物数量或订阅套餐数量"""

    event_timestamp: int = Field(default_factory=current_timestamp_ms)
    """交互行为发生时间戳，单位为毫秒"""

    created_at: int = Field(default_factory=current_timestamp_ms)
    """记录创建时间戳，单位为毫秒"""

    fields: dict[str, Any] = Field(default_factory=dict)
    """交互行为扩展字段"""


__all__ = [
    "Interaction",
]
