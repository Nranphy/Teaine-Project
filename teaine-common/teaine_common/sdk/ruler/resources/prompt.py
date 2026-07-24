from teaine_common.models.prompt import (
    PromptRenderResponse,
    PromptRenderRequest,
    PromptTemplateCreate,
    PromptTemplateRead,
    PromptTemplateUpdate,
)


class RulerPromptResource:
    def __init__(self, client):
        self._client = client

    async def create(self, prompt: PromptTemplateCreate) -> PromptTemplateRead:
        data = await self._client.request(
            "POST", "/api/v1/internal/prompt", json=prompt.model_dump()
        )
        return PromptTemplateRead.model_validate(data)

    async def delete(self, name: str) -> None:
        await self._client.request("DELETE", f"/api/v1/internal/prompt/{name}")

    async def update(
        self, name: str, prompt: PromptTemplateUpdate
    ) -> PromptTemplateRead:
        data = await self._client.request(
            "PUT", f"/api/v1/internal/prompt/{name}", json=prompt.model_dump()
        )
        return PromptTemplateRead.model_validate(data)

    async def render(
        self, name: str, params: dict[str, str] | None = None
    ) -> PromptRenderResponse:
        payload = PromptRenderRequest(params=params or {})
        data = await self._client.request(
            "POST",
            f"/api/v1/internal/prompt/{name}/render",
            json=payload.model_dump(),
        )
        return PromptRenderResponse.model_validate(data)


__all__ = ["RulerPromptResource"]
