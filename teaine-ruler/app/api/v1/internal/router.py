from fastapi import APIRouter

from .kms import router as kms_router
from .prompt import router as prompt_router
from .system import router as system_router
from .tool import router as tool_router

router = APIRouter(prefix="/internal")
router.include_router(system_router)
router.include_router(kms_router)
router.include_router(prompt_router)
router.include_router(tool_router)
__all__ = ["router"]
