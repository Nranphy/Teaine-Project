from teaine_common.models.corpus import Corpus, Message, Role


def test_corpus_builds_role_name_map():
    corpus = Corpus(
        data=[Message(role=Role(role_type="user", name=" Alice "), content=" hello ")]
    )
    assert corpus.data[0].content == "hello"
    assert corpus.role_name_map["Alice"] == "user"
