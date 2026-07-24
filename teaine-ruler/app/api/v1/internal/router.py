from fastapi import APIRouter

from .corpus import router as corpus_router
from .kms import router as kms_router
from .prompt import router as prompt_router
from .system import router as system_router

router = APIRouter(prefix="/internal")
router.include_router(system_router)
router.include_router(kms_router)
router.include_router(prompt_router)
router.include_router(corpus_router)
__all__ = ["router"]
