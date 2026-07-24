from enum import StrEnum


class ServiceEnum(StrEnum):
    ruler = "ruler"
    grail = "grail"
    caster = "caster"
    archer = "archer"
    rider = "rider"
    unknown = "unknown"


__all__ = ["ServiceEnum"]
