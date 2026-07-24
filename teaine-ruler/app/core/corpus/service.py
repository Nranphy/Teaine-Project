import hashlib
from asyncio import Lock
from collections import defaultdict
from pathlib import Path

import aiofiles
from teaine_common.models.corpus import Corpus, DatasetInfo


class CorpusService:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self._locks = defaultdict(Lock)

    def _dataset_dir(self, name: str) -> Path:
        if "/" in name or "\\" in name:
            raise ValueError("invalid dataset name")
        return self.data_dir / name

    def list(self) -> list[DatasetInfo]:
        return [
            self.get(path.name)
            for path in sorted(self.data_dir.iterdir())
            if path.is_dir() and (path / "INFO.json").exists()
        ]

    def get(self, name: str) -> DatasetInfo:
        path = self._dataset_dir(name) / "INFO.json"
        if not path.exists():
            raise FileNotFoundError(name)
        return DatasetInfo.model_validate_json(path.read_text(encoding="utf-8-sig"))

    def create(self, dataset: DatasetInfo) -> DatasetInfo:
        dataset_dir = self._dataset_dir(dataset.name)
        if dataset_dir.exists():
            raise FileExistsError(dataset.name)
        dataset_dir.mkdir(parents=True)
        (dataset_dir / "INFO.json").write_text(
            dataset.model_dump_json(), encoding="utf-8-sig"
        )
        return dataset

    async def add(self, dataset_name: str, corpus: Corpus) -> DatasetInfo:
        info = self.get(dataset_name)
        corpus_json = corpus.model_dump_json()
        bucket_id = (
            int(hashlib.sha256(corpus_json.encode()).hexdigest(), 16) % info.bucket_num
            + 1
        )
        path = self._dataset_dir(dataset_name) / f"bucket_{bucket_id}.jsonl"
        async with self._locks[path]:
            async with aiofiles.open(path, "a", encoding="utf-8-sig") as file:
                await file.write(corpus_json + "\n")
        return info


__all__ = ["CorpusService"]
