from fastapi import APIRouter, Depends, HTTPException
from teaine_common.models.kms import KmsEntry, KmsEntryCreate, KmsEntryUpdate

from app.core import get_services
from app.security.dependencies import require_internal_service

router = APIRouter(prefix="/kms", dependencies=[Depends(require_internal_service)])


@router.post("", response_model=KmsEntry)
async def create(entry: KmsEntryCreate) -> KmsEntry:
    return get_services().kms.create(entry)


@router.get("/{namespace}/{key}", response_model=KmsEntry)
async def get(namespace: str, key: str) -> KmsEntry:
    try:
        return get_services().kms.get(namespace, key)
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.put("/{namespace}/{key}", response_model=KmsEntry)
async def set_entry(namespace: str, key: str, entry: KmsEntryUpdate) -> KmsEntry:
    return get_services().kms.set(namespace, key, entry)
