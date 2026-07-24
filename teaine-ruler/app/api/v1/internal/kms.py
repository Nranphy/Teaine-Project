from fastapi import APIRouter, HTTPException
from teaine_common.models.kms import KmsEntry, KmsEntryUpdate

from app.services import get_services

router = APIRouter(prefix="/kms")


@router.get("/{namespace}/{key}", response_model=KmsEntry)
async def get(namespace: str, key: str) -> KmsEntry:
    try:
        return await get_services().kms.get(namespace, key)
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc


@router.put("/{namespace}/{key}", response_model=KmsEntry)
async def set_entry(namespace: str, key: str, entry: KmsEntryUpdate) -> KmsEntry:
    return await get_services().kms.set(namespace, key, entry)
