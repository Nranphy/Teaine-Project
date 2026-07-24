from fastapi import APIRouter
from teaine_common.models.system import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(service="ruler")
