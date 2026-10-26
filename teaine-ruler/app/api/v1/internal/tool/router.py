from fastapi import APIRouter

from .holidays import router as holidays_router


router = APIRouter(prefix="/tool")
router.include_router(holidays_router)

__all__ = ["router"]

