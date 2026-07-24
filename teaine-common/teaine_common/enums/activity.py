from enum import StrEnum


class ActivityTypeEnum(StrEnum):
    test = "test"
    live = "live"
    chat = "chat"
    tweet = "tweet"
    community = "community"
    unknown = "unknown"


class ActivitySegmentTypeEnum(StrEnum):
    test = "test"
    live_normal = "live_normal"
    live_private = "live_private"
    live_playgame = "live_playgame"
    live_readbook = "live_readbook"
    chat_private = "chat_private"
    chat_public = "chat_public"
    tweet = "tweet"
    community = "community"
    unknown = "unknown"


__all__ = ["ActivitySegmentTypeEnum", "ActivityTypeEnum"]
