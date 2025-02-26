# Subject Indexers

This repository provides two pipelines:

1) for processing text and label files in order to train and evaluate an Omikuji model. 
It includes text lemmatization, TF-IDF feature extraction, 
label binarization. The system is designed for extreme multilabel classification.
2) for processing text and extracting topic keywords using unsupervised methods.
Optionally multiword keyword detection can be enabled by using a pretrained PhraserModel.
Spelling mistakes can be automatically corrected by enabling SpellCorrector.

---

## ⚙️ Installation Guide

### Preparing the Environment

<details><summary>Click to expand</summary>

1. **Set Up Your Python Environment**  
   Ensure you have Python **3.10** or above installed.

2. **Install Required Dependencies**  
   Install the required dependencies using:
    ```bash
    pip install -r requirements.txt
    ```
</details>

---

## 🔮 Supervised Omikuji pipeline

<details><summary>Click to expand</summary>

### 🚀 Running the Pipeline

A sample code snippet to train and predict using the Omikuji model is provided below:

```python
from src.supervised.omikuji_model import OmikujiModel

model = OmikujiModel()  
# model.load(".../teemamarksonad_est") # Optionally load a pre-trained model and skip training

model.train(
    text_file="texts.txt",          # File with one document per line
    label_file="labels.txt",        # File with semicolon-separated labels for each document
    language="et",                  # Language of the text, in ISO 639-1 format
    lemmatization_required=True,    # (Optional) Whether to lemmatize the text - only set False if text_file is already lemmatized
    max_features=20000,             # (Optional) Maximum number of features for TF-IDF extraction
    keep_train_file=False,          # (Optional) Whether to retain intermediate training files
    eval_split=0.1                  # (Optional) Proportion of the dataset used for evaluation
)

predictions = model.predict(
    text="Kui Arno isaga koolimajja jõudis",  # Text to classify
    top_k=3                                   # Number of top predictions to return
)  # Output: [('koolimajad', 0.262), ('isad', 0.134), ('õpilased', 0.062)]
```

### 📂 Data Format

The files provided to the train function should be in the following format:
- A **text file** (`.txt`) where each line is a document.
    ```
    Document one content.
    Document two content.
    ```
- A **label file** (`.txt`) where each line contains semicolon-separated labels corresponding to the text file.
    ```
    label1;label2
    label3;label4
    ```

### 🛠 Components Overview

| Component | Description |
|-----------|-------------|
| `DataLoader` | Handles reading and preprocessing parallel text-label files. |
| `TfidfFeatureExtractor` | Extracts TF-IDF features from preprocessed text files. |
| `LabelBinarizer` | Encodes labels into a sparse binary matrix. |
| `TextPreprocessor` | Handles text preprocessing, including lemmatization. |
| `OmikujiModel` | Handles model training using Omikuji, a scalable extreme classification library. |
| `OmikujiHelpers` | Helper functions for Omikuji model training and evaluation. |

### 📝 Testing

Run the test suite:
```bash
python -m pytest -v tests
```

</details>

## ⛓️‍💥 Unsupervised RaKUn + Phraser pipeline

<details><summary>Click to expand</summary>

### 🚀 Running the Pipeline

A sample code snippet to extract keywords from a random text is provided below:

```python
from src.unsupervised.unsup_kw_extractor import KeywordExtractor
from symspellpy import Verbosity

model = KeywordExtractor()  # Optionally provide model_artifacts_path to load a pre-trained model.

predictions = model.predict(
    text="Kui Arno isaga ...",  # Text to classify
    lang_code="et",             # (Optional) Language of the text, in ISO 639-1 format, if not provided, language is detected automatically
    top_n=10,                   # Number of top predictions to return
    merge_threshold=0.0,        # (Optional) Threshold for merging words into a single keyword. If 0.0 no words are merged.
    use_phraser=True,           # (Optional) Whether to use phraser or not. Available Phraser models must be defined in constants.py
    correct_spelling=True,      # (Optional) Whether to use spell correction or not.
    preserve_case=True,         # (Optional) Whether to preserve original case or not.
    max_uppercase=2,            # (Optional) The maximum number of uppercase letters in the word to allow spelling correction.
    min_word_frequency=3,       # (Optional) The minimum frequency of the word in the input text required for it to NOT be corrected using spelling correction.
)  # Output: ['koolimaja']
```

A sample code snippet to train and predict using the Phraser model is provided below:

```python
from src.unsupervised.phraser_model import PhraserModel

model = PhraserModel()

model.train(
    train_data_path=".../train.txt",  # File with one document per line, text should be lemmatised.
    lang_code="et",                      # Language of the text, in ISO 639-1 format
    min_count=5,                         # (Optional) Minimum word frequency for phrase formation.
    threshold=10.0                       # (Optional) Score threshold for forming phrases.
)

predictions = model.predict(
    text="'vabariik aastapäev sööma kiluvõileib'",  # Lemmatised text for phrase detection
)  # Output: ['vabariik_aastapäev', 'sööma', kiluvõileib']
```

### 📂 Data Format

The file provided to the PhraserModel train function should be in the following format:

- A **text file** (`.txt`) where each line is a document.
    ```
    Document one content.
    Document two content.
    ```

### 🛠 Components Overview

| Component          | Description                                                                                                                                                                                                           |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `KeywordExtractor` | Extracts topic keywords from the text using unsupervised methods. Optionally multi-word keywords can be found using a pretrained PhraserModel. Spelling mistakes can be automatically corrected using SpellCorrector. |
| `PhraserModel`     | Handles Gensim Phraser model training and evaluation.                                                                                                                                                                 |
| `SpellCorrector`   | Handles spelling correction logic using SymSpell.                                                                                                                                                                     |                                                         |

---

</details>