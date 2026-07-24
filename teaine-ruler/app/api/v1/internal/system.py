from fastapi import APIRouter, Depends
from teaine_common.models.system import SystemInfo

from app.core import get_services
from app.security.dependencies import require_internal_service

router = APIRouter(prefix="/system", dependencies=[Depends(require_internal_service)])


@router.get("/info", response_model=SystemInfo)
async def info() -> SystemInfo:
    return get_services().system.info()
