"""定义通用的枚举组件"""

from enum import StrEnum


class Platform(StrEnum):
    """媒体平台枚举"""

    system = 'system'
    '''系统'''

    bilibili = 'bilibili'
    '''Bilibili'''

    douyin = 'douyin'
    '''抖音'''

    tiktok = 'tiktok'
    '''Tiktok'''

    youtube = 'youtube'
    '''Youtube'''

    unknown = 'unknown'
    '''未知平台'''


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


class SceneType(StrEnum):
    """应用场景类型枚举"""

    test = 'test'
    '''测试场景'''

    live_normal = 'live_normal'
    '''
    普通直播场景
    
    表示普通的针对用户互动行为进行响应的直播场景
    '''

    live_private = 'live_private'
    '''
    封闭直播场景

    表示对模型的输入是可控的直播场景，如开发者对话、联动、外景等
    '''

    live_readbook = 'live_readbook'
    '''
    读书会直播场景
    '''

    live_playgame = 'live_playgame'
    '''
    游戏直播场景
    '''

    chat_private = 'chat_private'
    '''
    私人聊天场景
    
    只有单个其他聊天参与人的聊天场景
    '''

    chat_public = 'chat_public'
    '''
    公共聊天场景
    
    有多个其他聊天参与人的聊天场景
    '''

    tweet = 'tweet'
    '''
    推文生成场景
    
    仅指代生成推文的过程，不包括推文的回复
    '''

    community = 'community'
    '''
    社区场景
    
    社区内容的回复、评论等，包括对自身内容的回复
    '''

    unknown = 'unknown'
    '''未知场景'''


__all__ = [
    "Platform",
    "InteractionType",
    "SceneType",
]
