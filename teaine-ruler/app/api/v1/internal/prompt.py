from fastapi import APIRouter, Depends, HTTPException
from pydantic import Field
from teaine_common.models.base import TeaineModel
from teaine_common.models.prompt import (
    PromptRenderResponse,
    PromptTemplateCreate,
    PromptTemplateListResponse,
    PromptTemplateRead,
)

from app.core import get_services
from app.security.dependencies import require_internal_service


class PromptRenderBody(TeaineModel):
    params: dict[str, str] = Field(default_factory=dict)


router = APIRouter(prefix="/prompt", dependencies=[Depends(require_internal_service)])


@router.get("", response_model=PromptTemplateListResponse)
async def list_prompts() -> PromptTemplateListResponse:
    return get_services().prompt.list()


@router.post("", response_model=PromptTemplateRead)
async def create_prompt(prompt: PromptTemplateCreate) -> PromptTemplateRead:
    try:
        return get_services().prompt.create(prompt)
    except FileExistsError as exc:
        raise HTTPException(409, "prompt already exists") from exc


@router.get("/{name}", response_model=PromptTemplateRead)
async def get_prompt(name: str) -> PromptTemplateRead:
    try:
        return get_services().prompt.get(name)
    except FileNotFoundError as exc:
        raise HTTPException(404, "prompt not found") from exc


@router.post("/{name}/render", response_model=PromptRenderResponse)
async def render_prompt(name: str, body: PromptRenderBody) -> PromptRenderResponse:
    try:
        return get_services().prompt.render(name, body.params)
    except FileNotFoundError as exc:
        raise HTTPException(404, "prompt not found") from exc
