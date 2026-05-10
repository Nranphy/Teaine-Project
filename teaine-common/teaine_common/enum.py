"""定义通用的枚举组件"""

from enum import StrEnum


class PlatformEnum(StrEnum):
    """媒体平台枚举"""

    system = 'system'
    """系统"""
    bilibili = 'bilibili'
    """Bilibili"""
    douyin = 'douyin'
    """抖音"""
    tiktok = 'tiktok'
    """Tiktok"""
    youtube = 'youtube'
    """Youtube"""
    unknown = 'unknown'
    """未知平台"""


class InteractionType(StrEnum):
    """交互行为类型枚举"""

    live_chat = 'live_chat'
    """直播普通弹幕"""
    live_super_chat = 'live_super_chat'
    """直播醒目留言"""
    live_gift = 'live_gift'
    """直播礼物"""
    live_premium = 'live_premium'
    """直播付费订阅"""
    unknown = 'unknown'
    """未知"""


class ActivityTypeEnum(StrEnum):
    """业务活动类型枚举"""

    test = 'test'
    """测试活动"""

    live = 'live'
    """直播活动"""

    chat = 'chat'
    """对话活动"""

    tweet = 'tweet'
    """推文活动"""

    community = 'community'
    """社区活动"""

    unknown = 'unknown'
    """未知活动"""


class ActivitySegmentTypeEnum(StrEnum):
    """业务活动阶段类型枚举"""

    test = 'test'
    """测试阶段"""

    live_normal = 'live_normal'
    """
    普通直播阶段
    
    表示普通的针对用户互动行为进行响应的直播阶段
    """

    live_private = 'live_private'
    """
    封闭直播阶段

    表示对模型的输入是可控的直播阶段，如开发者对话、联动、外景等
    """

    live_playgame = 'live_playgame'
    """
    游戏直播阶段
    """

    live_readbook = 'live_readbook'
    """
    读书会直播阶段
    """

    chat_private = 'chat_private'
    """
    私人聊天阶段
    
    只有单个其他聊天参与人的聊天阶段
    """

    chat_public = 'chat_public'
    """
    公共聊天阶段
    
    有多个其他聊天参与人的聊天阶段
    """

    tweet = 'tweet'
    """
    推文生成阶段
    
    仅指代生成推文的过程，不包括推文的回复
    """

    community = 'community'
    """
    社区阶段
    
    社区内容的回复、评论等，包括对自身内容的回复
    """

    unknown = 'unknown'
    """未知阶段"""


__all__ = [
    'PlatformEnum',
    'InteractionType',
    'ActivityTypeEnum',
    'ActivitySegmentTypeEnum',
]
