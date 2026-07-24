from pydantic import Field

from teaine_common.models.base import TeaineModel


class PromptTemplate(TeaineModel):
    name: str
    description: str = ""
    content: str
    params: str = ""


class PromptTemplateCreate(PromptTemplate):
    pass


class PromptTemplateUpdate(TeaineModel):
    description: str = ""
    content: str
    params: str = ""


class PromptRenderRequest(TeaineModel):
    params: dict[str, str] = Field(default_factory=dict)


class PromptRenderResponse(TeaineModel):
    name: str
    text: str


PromptTemplateRead = PromptTemplate

BasePrompt = PromptTemplate
BasePromptAdd = PromptTemplateCreate
BasePromptGet = PromptRenderRequest
BasePromptInfo = PromptTemplate

__all__ = [
    "BasePrompt",
    "BasePromptAdd",
    "BasePromptGet",
    "BasePromptInfo",
    "PromptRenderRequest",
    "PromptRenderResponse",
    "PromptTemplate",
    "PromptTemplateCreate",
    "PromptTemplateRead",
    "PromptTemplateUpdate",
]
