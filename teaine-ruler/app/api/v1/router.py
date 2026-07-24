from fastapi import APIRouter

from .internal.router import router as internal_router
from .public.router import router as public_router

router = APIRouter(prefix="/v1")
router.include_router(public_router)
router.include_router(internal_router)
__all__ = ["router"]
