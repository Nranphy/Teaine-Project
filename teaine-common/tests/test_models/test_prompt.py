from teaine_common.models.prompt import PromptTemplate


def test_prompt_template_renders_params():
    prompt = PromptTemplate(
        name="hello", text="你好，{{{name}}}", params={"name": "茶因"}
    )
    assert prompt.text == "你好，茶因"
