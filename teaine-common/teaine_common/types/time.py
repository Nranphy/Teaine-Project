from datetime import UTC, datetime
from typing import NewType

MillisecondsTimestamp = NewType("MillisecondsTimestamp", int)


def current_timestamp_ms() -> int:
    return int(datetime.now(UTC).timestamp() * 1000)


__all__ = ["MillisecondsTimestamp", "current_timestamp_ms"]
