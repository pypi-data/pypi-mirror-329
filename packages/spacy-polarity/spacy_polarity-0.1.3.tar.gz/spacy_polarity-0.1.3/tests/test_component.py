import pytest
import spacy
from textblob import TextBlob

import spacy_polarity  # noqa: F401
from spacy_polarity._transformers import Model, polarity


@pytest.fixture()
def document() -> str:
    return (
        "The financial markets are performing well, bringing good returns to investors. "
        "The stock markets in USA grew by 5% this year."
    )


@pytest.fixture()
def nlp():
    model = spacy.load("en_core_web_sm")
    model.add_pipe("spacy_polarity")
    return model


@pytest.fixture()
def nlp_transformer():
    model = spacy.load("en_core_web_sm")

    model.add_pipe("spacy_polarity", config={"use_transformer": True})

    return model


def test_component_with_textblob(document, nlp):
    doc = nlp(document)
    results = [sentence._.polarity for sentence in doc.sents]
    expected = list(
        map(lambda sentence: TextBlob(sentence).polarity, document.split(". "))
    )
    assert results == expected
    doc._.polarity == TextBlob(document).polarity


def test_component_with_transformer(document, nlp_transformer):
    doc = nlp_transformer(document)
    sentences = list(doc.sents)
    results = [sentence._.polarity for sentence in sentences]
    print([sent.text for sent in sentences])
    model = Model()

    expected_sentences = [
        "The financial markets are performing well, bringing good returns to investors.",
        "The stock markets in USA grew by 5% this year.",
    ]
    expected = [polarity(item) for item in model(expected_sentences)]
    assert results == expected
