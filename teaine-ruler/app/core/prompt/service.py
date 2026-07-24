import re
from pathlib import Path

from teaine_common.models.prompt import (
    PromptRenderResponse,
    PromptTemplateCreate,
    PromptTemplateListResponse,
    PromptTemplateRead,
    PromptTemplateStatus,
)

from .renderer import render_prompt


class PromptService:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def _path(self, name: str) -> Path:
        if "/" in name or "\\" in name:
            raise ValueError("invalid prompt name")
        return self.data_dir / f"{name}.txt"

    def list(self) -> PromptTemplateListResponse:
        prompts = []
        for path in sorted(self.data_dir.glob("*.txt")):
            text = path.read_text(encoding="utf-8-sig").strip()
            prompts.append(
                PromptTemplateStatus(
                    name=path.stem,
                    length=len(text),
                    param_num=len(re.findall(r"{{{[A-Za-z]+?}}}", text)),
                )
            )
        return PromptTemplateListResponse(prompts=prompts)

    def create(self, payload: PromptTemplateCreate) -> PromptTemplateRead:
        path = self._path(payload.name)
        if path.exists():
            raise FileExistsError(payload.name)
        path.write_text(payload.text, encoding="utf-8-sig")
        return PromptTemplateRead(name=payload.name, text=payload.text)

    def get(self, name: str) -> PromptTemplateRead:
        path = self._path(name)
        if not path.exists():
            raise FileNotFoundError(name)
        return PromptTemplateRead(
            name=name, text=path.read_text(encoding="utf-8-sig").strip()
        )

    def render(self, name: str, params: dict[str, str]) -> PromptRenderResponse:
        prompt = self.get(name)
        return PromptRenderResponse(
            name=name, text=render_prompt(name, prompt.text, params)
        )


__all__ = ["PromptService"]
