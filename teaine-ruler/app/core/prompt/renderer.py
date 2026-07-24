from teaine_common.models.prompt import PromptTemplate


def render_prompt(name: str, text: str, params: dict[str, str]) -> str:
    return PromptTemplate(name=name, text=text, params=params).text


__all__ = ["render_prompt"]
