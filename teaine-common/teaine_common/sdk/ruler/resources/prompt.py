from teaine_common.models.prompt import (
    PromptRenderResponse,
    PromptTemplateCreate,
    PromptTemplateListResponse,
    PromptTemplateRead,
)


class RulerPromptResource:
    def __init__(self, client):
        self._client = client

    async def list(self) -> PromptTemplateListResponse:
        data = await self._client.request("GET", "/api/v1/internal/prompt")
        return PromptTemplateListResponse.model_validate(data)

    async def create(self, prompt: PromptTemplateCreate) -> PromptTemplateRead:
        data = await self._client.request(
            "POST", "/api/v1/internal/prompt", json=prompt.model_dump()
        )
        return PromptTemplateRead.model_validate(data)

    async def render(
        self, name: str, params: dict[str, str] | None = None
    ) -> PromptRenderResponse:
        data = await self._client.request(
            "POST",
            f"/api/v1/internal/prompt/{name}/render",
            json={"params": params or {}},
        )
        return PromptRenderResponse.model_validate(data)


__all__ = ["RulerPromptResource"]
