from fastapi import APIRouter, Depends, HTTPException
from teaine_common.models.corpus import CorpusAdd, DatasetInfo

from app.core import get_services
from app.security.dependencies import require_internal_service

router = APIRouter(prefix="/corpus", dependencies=[Depends(require_internal_service)])


@router.get("", response_model=list[DatasetInfo])
async def list_datasets() -> list[DatasetInfo]:
    return get_services().corpus.list()


@router.post("", response_model=DatasetInfo)
async def create_dataset(dataset: DatasetInfo) -> DatasetInfo:
    try:
        return get_services().corpus.create(dataset)
    except FileExistsError as exc:
        raise HTTPException(409, "dataset already exists") from exc


@router.get("/{name}", response_model=DatasetInfo)
async def get_dataset(name: str) -> DatasetInfo:
    try:
        return get_services().corpus.get(name)
    except FileNotFoundError as exc:
        raise HTTPException(404, "dataset not found") from exc


@router.post("/items", response_model=DatasetInfo)
async def add_corpus(payload: CorpusAdd) -> DatasetInfo:
    try:
        return await get_services().corpus.add(payload.dataset_name, payload.corpus)
    except FileNotFoundError as exc:
        raise HTTPException(404, "dataset not found") from exc
