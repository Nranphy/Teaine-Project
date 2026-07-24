from fastapi import APIRouter, HTTPException
from teaine_common.models.prompt import (
    PromptRenderRequest,
    PromptRenderResponse,
    PromptTemplateCreate,
    PromptTemplateRead,
    PromptTemplateUpdate,
)

from app.services import get_services


router = APIRouter(prefix="/prompt")


@router.post("", response_model=PromptTemplateRead)
async def create_prompt(prompt: PromptTemplateCreate) -> PromptTemplateRead:
    try:
        return await get_services().prompt.create(prompt)
    except FileExistsError as exc:
        raise HTTPException(409, "prompt already exists") from exc


@router.delete("/{name}", status_code=204)
async def delete_prompt(name: str) -> None:
    try:
        await get_services().prompt.delete(name)
    except FileNotFoundError as exc:
        raise HTTPException(404, "prompt not found") from exc


@router.put("/{name}", response_model=PromptTemplateRead)
async def update_prompt(
    name: str, prompt: PromptTemplateUpdate
) -> PromptTemplateRead:
    try:
        return await get_services().prompt.update(name, prompt)
    except FileNotFoundError as exc:
        raise HTTPException(404, "prompt not found") from exc


@router.post("/{name}/render", response_model=PromptRenderResponse)
async def render_prompt(
    name: str, body: PromptRenderRequest
) -> PromptRenderResponse:
    try:
        return await get_services().prompt.render(name, body.params)
    except FileNotFoundError as exc:
        raise HTTPException(404, "prompt not found") from exc
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
