from enum import StrEnum


class InteractionType(StrEnum):
    live_chat = "live_chat"
    live_super_chat = "live_super_chat"
    live_gift = "live_gift"
    live_premium = "live_premium"
    unknown = "unknown"


__all__ = ["InteractionType"]
