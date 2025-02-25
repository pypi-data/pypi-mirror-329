import torch
from transformers import pipeline

from spacy_polarity._transformers import Model


def test_model():
    sentence = "The financial markets are performing well, bringing good returns to investors. The stock markets in USA grew by 5% this year."

    model = Model("ProsusAI/finbert")

    output_item = model([sentence])[0]
    label_idx = int(torch.argmax(output_item["probabilities"]))
    label = output_item["id2label"][label_idx]
    score = torch.max(output_item["probabilities"])

    nlp = pipeline(model="ProsusAI/finbert", task="text-classification")
    expected = nlp([sentence])[0]
    expected_label = expected["label"]
    expected_score = expected["score"]

    assert label == expected_label
    assert score == expected_score
