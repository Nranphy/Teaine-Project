from fastapi import APIRouter
from teaine_common.models.system import SystemInfo

from app.services import get_services

router = APIRouter(prefix="/system")


@router.get("/info", response_model=SystemInfo)
async def info() -> SystemInfo:
    return await get_services().system.info()
