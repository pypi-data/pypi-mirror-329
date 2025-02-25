from typing import Dict, List, Literal, TypeAlias, TypedDict

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class ModelOutputItem(TypedDict):
    probabilities: torch.Tensor
    id2label: Dict[int, str]


ModelOutput: TypeAlias = List[ModelOutputItem]


def polarity(item: ModelOutputItem) -> List[str]:
    probs = item["probabilities"]
    id2label = item["id2label"]
    inverted = {v: k for k, v in id2label.items()}
    assert "neutral" in inverted
    assert "positive" in inverted
    assert "negative" in inverted
    return probs[inverted["positive"]] - probs[inverted["negative"]]


class Model:
    def __init__(
        self,
        name: Literal["ProsusAI/finbert"] = "ProsusAI/finbert",
        padding: bool = True,
        truncation: bool = True,
        use_gpu: bool = False,
    ):
        self.tokenizer = AutoTokenizer.from_pretrained(name)
        self.model = AutoModelForSequenceClassification.from_pretrained(name)
        self._padding = padding
        self._truncation = truncation
        self.name = name
        self.device = torch.device(
            "cuda" if use_gpu and torch.cuda.is_available() else "cpu"
        )
        self.model.to(self.device)

    def _process(self, output, name: Literal["ProsusAI/finbert"]) -> ModelOutput:
        if name != "ProsusAI/finbert":
            raise ValueError(
                f"Unsupported model: {name}. Only 'ProsusAI/finbert' is supported."
            )

        probs = torch.softmax(output.logits, dim=-1)

        id2label = self.model.config.id2label

        model_output: ModelOutput = [
            {"probabilities": probs[i].to("cpu"), "id2label": id2label}
            for i in range(probs.shape[0])
        ]

        return model_output

    def __call__(self, docs: List[str]) -> ModelOutput:
        """Process a list of documents and return model output with probabilities."""
        tokenized = self.tokenizer(
            docs,
            padding=self._padding,
            truncation=self._truncation,
            return_tensors="pt",
        )

        tokenized = {key: val.to(self.device) for key, val in tokenized.items()}

        with torch.no_grad():
            output = self.model(**tokenized)
        return self._process(output, self.name)
