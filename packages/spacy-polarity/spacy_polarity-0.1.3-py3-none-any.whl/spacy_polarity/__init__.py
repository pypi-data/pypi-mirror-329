from abc import ABCMeta, abstractmethod
from functools import cached_property
from typing import Iterable

from spacy.language import Language
from spacy.tokens.doc import Doc
from spacy.tokens.span import Span
from textblob import TextBlob

from spacy_polarity._version import __version__
from spacy_polarity.types import SpacyPolarityConfig, TextBlobConfig, TransformerConfig


class PolarityABC(metaclass=ABCMeta):
    def __init__(
        self,
        has_sentencizer: bool,
        use_transformer: bool,
        textblob_config: TextBlobConfig,
        transformer_config: TransformerConfig,
    ):
        self.textblob_config = textblob_config
        self.transformer_config = transformer_config
        self.use_transformer = use_transformer
        self.has_sentencizer = has_sentencizer
        self.__post__init__()

    @abstractmethod
    def __call__(self, doc: Doc) -> Doc: ...

    @abstractmethod
    def __post__init__(self): ...


class HierarchicalPolarity(PolarityABC):
    @staticmethod
    def _textblob_infer(doc: Doc, has_sentencizer: bool, config: TextBlobConfig):
        sentences: Iterable[Span] = doc.sents
        if has_sentencizer:
            for sentence in sentences:
                textblob = TextBlob(sentence.text, **config)
                sentence._.polarity = textblob.polarity
        doc._.polarity = TextBlob(doc.text).polarity

    def _transformer_infer(
        self, doc: Doc, has_sentencizer: bool, config: TransformerConfig
    ):
        from spacy_polarity._transformers import polarity

        sentences: Iterable[Span] = doc.sents
        sentences = list(sentences)
        if has_sentencizer:
            output = self.model([sentence.text for sentence in sentences])
            for i, sentence in enumerate(sentences):
                sentence._.polarity = polarity(output[i])
        output = self.model([doc.text])
        doc._.polarity = polarity(output[0])

    @cached_property
    def model(self) -> "spacy_polarity._transformers.Model":  # noqa: F821
        from spacy_polarity._transformers import Model

        return Model(**self.transformer_config)

    def __call__(self, doc: Doc) -> Doc:
        if not self.use_transformer:
            self._textblob_infer(doc, self.has_sentencizer, self.textblob_config)
        else:
            self._transformer_infer(doc, self.has_sentencizer, self.transformer_config)
        return doc

    def __post__init__(self):
        if not Doc.has_extension("polarity"):
            Doc.set_extension("polarity", default=None)
        if not Span.has_extension("polarity"):
            Span.set_extension("polarity", default=None)


def hierarchical_polarity(
    nlp: Language,
    name: str,
    sentence_polarity: bool,
    use_transformer: bool,
    textblob_config: TextBlobConfig,
    transformer_config: TransformerConfig,
):
    has_sentencizer = "senter" in nlp.component_names and sentence_polarity
    return HierarchicalPolarity(
        has_sentencizer,
        use_transformer,
        textblob_config=textblob_config,
        transformer_config=transformer_config,
    )


DEFAULT_CONFIG: SpacyPolarityConfig = {
    # Whether to apply sentence polarity
    "sentence_polarity": True,
    "use_transformer": False,
    "textblob_config": {
        "tokenizer": None,
        "np_extractor": None,
        "pos_tagger": None,
        "analyzer": None,
        "parser": None,
        "classifier": None,
    },
    "transformer_config": {
        "name": "ProsusAI/finbert",
        "padding": True,
        "truncation": True,
        "use_gpu": False,
    },
}


Language.factory(
    "spacy_polarity",
    default_config=DEFAULT_CONFIG,
    func=hierarchical_polarity,
)


__all__ = ["__version__", "DEFAULT_CONFIG", "HierarchicalPolarity"]
