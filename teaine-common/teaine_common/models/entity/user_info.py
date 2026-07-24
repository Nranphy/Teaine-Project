"""用户信息实体模型"""

from typing import Any

from pydantic import Field

from teaine_common.enum import PlatformEnum

from .base import EntityModel, current_timestamp_ms


class UserInfo(EntityModel):
    """用户账号系统的基本信息和平台特有信息"""

    id: int | None = None
    """用户账号系统 ID"""

    main_id: int | None = None
    """用户主账号系统 ID，用于跨平台账号绑定，未绑定时为空"""

    platform: PlatformEnum
    """用户账号所属媒体平台"""

    platform_user_id: str
    """用户在对应媒体平台上的唯一账号 ID"""

    platform_user_name: str = ""
    """用户在对应媒体平台上的昵称"""

    platform_fields: dict[str, Any] = Field(default_factory=dict)
    """用户账号的平台特有信息字段"""

    description: str = ""
    """用户描述，用于补充昵称、曾用名、经历、情感等认知信息"""

    register_timestamp: int = Field(default_factory=current_timestamp_ms)
    """用户注册或首次记录时间戳，单位为毫秒"""


__all__ = [
    "UserInfo",
]
