import re

from pydantic import Field, model_validator

from teaine_common.models.base import TeaineModel


class PromptTemplate(TeaineModel):
    name: str
    text: str
    params: dict[str, str] = Field(default_factory=dict)

    @model_validator(mode="after")
    def render_params(self):
        if not self.params:
            return self
        pattern = re.compile(
            r"\{\{\{("
            + "|".join(map(re.escape, sorted(self.params, key=len, reverse=True)))
            + r")\}\}\}"
        )
        self.text = pattern.sub(lambda m: str(self.params[m.group(1)]), self.text)
        return self


class PromptTemplateCreate(TeaineModel):
    name: str
    text: str


class PromptTemplateRead(TeaineModel):
    name: str
    text: str


class PromptTemplateStatus(TeaineModel):
    name: str
    length: int
    param_num: int


class PromptRenderRequest(TeaineModel):
    name: str
    params: dict[str, str] = Field(default_factory=dict)


class PromptRenderResponse(TeaineModel):
    name: str
    text: str


class PromptTemplateListResponse(TeaineModel):
    prompts: list[PromptTemplateStatus]


BasePrompt = PromptTemplate
BasePromptAdd = PromptTemplateCreate
BasePromptGet = PromptRenderRequest
BasePromptGetAll = TeaineModel
BasePromptInfo = PromptTemplateStatus
BasePromptManagerStatus = PromptTemplateListResponse

__all__ = [
    "BasePrompt",
    "BasePromptAdd",
    "BasePromptGet",
    "BasePromptGetAll",
    "BasePromptInfo",
    "BasePromptManagerStatus",
    "PromptRenderRequest",
    "PromptRenderResponse",
    "PromptTemplate",
    "PromptTemplateCreate",
    "PromptTemplateListResponse",
    "PromptTemplateRead",
    "PromptTemplateStatus",
]
