from typing import NewType

EntityId = NewType("EntityId", int)
ServiceName = NewType("ServiceName", str)

__all__ = ["EntityId", "ServiceName"]
