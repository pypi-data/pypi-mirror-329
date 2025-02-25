from typing import Literal, Optional, TypedDict


class TextBlobConfig(TypedDict):
    """
    Refer to `textblob documentation <https://textblob.readthedocs.io/en/dev/api_reference.html#textblob.blob.TextBlob>`_
    """

    tokenizer: Optional[object]
    np_extractor: Optional[object]
    pos_tagger: Optional[object]
    analyzer: Optional[object]
    parser: Optional[object]
    classifier: Optional[object]


class TransformerConfig(TypedDict):
    name: Literal["ProsusAI/finbert"]
    padding: bool
    truncation: bool
    use_gpu: bool


class SpacyPolarityConfig(TypedDict):
    """Whether to calculate the polarity for each sentence"""

    sentence_polarity: bool
    """Whether to use transformer or not"""
    use_transformer: bool
    """Refer to :py:class:`spacy_polarity.types.TextBlobConfig`"""
    textblob_config: TextBlobConfig
    transformer_config: TransformerConfig
