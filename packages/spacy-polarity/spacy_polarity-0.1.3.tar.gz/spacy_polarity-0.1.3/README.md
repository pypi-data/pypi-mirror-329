# spacy-polarity

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)  
![License](https://img.shields.io/badge/license-MIT-green.svg)  

**Measure sentiment polarity of sentences and documents with spaCy**

`spacy-polarity` is a spaCy pipeline component that adds sentiment polarity analysis to your pipeline. It supports both TextBlob-based polarity scoring and transformer-based sentiment analysis.

## Installation

Install `spacy-polarity` via pip:

```bash
pip install spacy-polarity
```

You’ll also need a spaCy language model (e.g., `en_core_web_sm`):

```bash
python -m spacy download en_core_web_sm
```

For transformer support, ensure you have `transformers` installed:

```bash
pip install "spacy-polarity[transformers]" 
```

## Usage

### Using TextBlob for Polarity

Analyze sentiment polarity with TextBlob’s lightweight algorithm:

```python
import spacy
import spacy_polarity

# Load spaCy model and add the polarity component
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("spacy_polarity")

# Process text
doc = nlp("The financial markets are performing well, bringing good returns to investors. The stock markets in USA grew by 5% this year.")

# Polarity for each sentence
for sent in doc.sents:
    print(f"Sentence: {sent.text}")
    print(f"Polarity: {sent._.polarity:.3f}\n")

# Polarity for the entire document
print(f"Document Polarity: {doc._.polarity:.3f}")
```

### Using Transformers

Leverage transformer models for more advanced sentiment analysis:

```python
import spacy
import spacy_polarity

# Load spaCy model and add the polarity component with transformers
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("spacy_polarity", config={"use_transformer": True})

# Process text
doc = nlp("The financial markets are performing well, bringing good returns to investors. The stock markets in USA grew by 5% this year.")

# Polarity for each sentence
for sent in doc.sents:
    print(f"Sentence: {sent.text}")
    print(f"Polarity: {sent._.polarity:.3f}\n")

# Polarity for the entire document
print(f"Document Polarity: {doc._.polarity:.3f}")
```

#### Performance Note

This package processes documents individually and does not batch inference across multiple documents. For high-volume analysis or GPU optimization, consider a custom solution using the `transformers` library directly.


## Development

### Style and Linting

Ensure code quality with `ruff`:

```bash
ruff check
ruff format
```

### Testing

Install test dependencies and run tests:

```bash
pip install ".[test]"
pytest -vvv
```

### ARM Installation

For ARM architectures (e.g., Raspberry Pi, Apple M1), use the following:

```bash
apt install python3-dev
pip install wheel
BLIS_ARCH="generic" pip install spacy --no-binary blis
pip install spacy-polarity
```

