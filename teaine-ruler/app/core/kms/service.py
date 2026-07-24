import json
from pathlib import Path
from threading import RLock

from teaine_common.models.kms import KmsEntry, KmsEntryCreate, KmsEntryUpdate
from teaine_common.version import __version__


class KmsService:
    def __init__(self, data_file: Path):
        self.data_file = data_file
        self._lock = RLock()
        if not self.data_file.exists():
            self._write(
                {"system": {"common_version": {"value": __version__, "metadata": {}}}}
            )

    def _read(self) -> dict:
        return (
            json.loads(self.data_file.read_text(encoding="utf-8"))
            if self.data_file.exists()
            else {}
        )

    def _write(self, data: dict) -> None:
        self.data_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def get(self, namespace: str, key: str) -> KmsEntry:
        with self._lock:
            data = self._read()
            try:
                item = data[namespace][key]
            except KeyError as exc:
                raise KeyError(f"KMS entry not found: {namespace}/{key}") from exc
            return KmsEntry(
                namespace=namespace,
                key=key,
                value=item["value"],
                metadata=item.get("metadata", {}),
            )

    def set(self, namespace: str, key: str, payload: KmsEntryUpdate) -> KmsEntry:
        with self._lock:
            data = self._read()
            data.setdefault(namespace, {})[key] = {
                "value": payload.value,
                "metadata": payload.metadata,
            }
            self._write(data)
            return self.get(namespace, key)

    def create(self, payload: KmsEntryCreate) -> KmsEntry:
        return self.set(
            payload.namespace,
            payload.key,
            KmsEntryUpdate(value=payload.value, metadata=payload.metadata),
        )


__all__ = ["KmsService"]
