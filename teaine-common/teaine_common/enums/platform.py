from enum import StrEnum


class PlatformEnum(StrEnum):
    system = "system"
    bilibili = "bilibili"
    douyin = "douyin"
    tiktok = "tiktok"
    youtube = "youtube"
    unknown = "unknown"


__all__ = ["PlatformEnum"]
