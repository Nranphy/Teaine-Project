from teaine_common.models.prompt import PromptTemplate


def test_prompt_template_keeps_database_fields():
    prompt = PromptTemplate(
        name="hello",
        description="greeting",
        content="你好，{{{name}}}",
        params="name",
    )
    assert prompt.name == "hello"
    assert prompt.description == "greeting"
    assert prompt.content == "你好，{{{name}}}"
    assert prompt.params == "name"
