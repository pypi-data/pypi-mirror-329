import os
import re
from typing import Iterator

from gensim.models.phrases import Phrases, Phraser
from gensim.utils import simple_preprocess, tokenize
from src.utils.constants import SUPPORTED_STOPWORDS_PHRASER, SENTENCE_SPLIT_REGEX


class PhraserModel:
    """
    A class for training, saving, loading and using Phraser models.
    """

    def __init__(self):
        """
        Initialize with stopwords loaded from constants.py.
        """
        self.stopwords = SUPPORTED_STOPWORDS_PHRASER
        self.model = None

    def train(self, train_data_path: str, lang_code: str, min_count: int = 5, threshold: float = 10.0):
        """
        Train a Phrases model for phrase detection.

        Parameters
        ----------
        train_data_path: str
            Path to the training data (plain text file).
        lang_code: str
            Language code (e.g., "en", "et").
        min_count: int, default 5
            Minimum word frequency for phrase formation.
        threshold: float, default 10.0
            Score threshold for forming phrases.
        """
        sentences = self._sentence_iterator(train_data_path)
        phrases = Phrases(
            sentences, min_count=min_count, threshold=threshold, connector_words=self.stopwords.get(lang_code, [])
        )
        self.model = Phraser(phrases)
        print("Training complete. Model not yet saved.")

    def _sentence_iterator(self, filepath: str) -> Iterator[str]:
        """
        Iterator for tokenized sentences from a plain text file.
        
        Parameters
        ----------
        filepath: str
            The path to the training data file.

        Returns
        -------
        Iterator[str]
            The tokenized sentences.
        """
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    yield from (list(
                        simple_preprocess(sentence) for sentence in re.split(SENTENCE_SPLIT_REGEX, line) if sentence))

    def save(self, model_save_path: str):
        """
        Save the trained model to the specified path.
        
        Parameters
        ----------
        model_save_path: str
            Path where the model will be saved.
        """
        if self.model:
            if os.path.exists(model_save_path):
                raise FileExistsError(f"Error: File already exists at {model_save_path}.")
            os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
            self.model.save(model_save_path)
            print(f"Model saved at {model_save_path}.")
        else:
            print("Model not trained. Cannot save.")

    def load(self, model_path: str):
        """
        Load a trained Phraser model from a file.

        Parameters
        ----------
            model_path: str
                Path where the trained model is stored.
        """
        try:
            self.model = Phraser.load(model_path)
            print(f"Model loaded from {model_path}.")
        except Exception as e:
            print(f"Error loading model: {e}")

    def predict(self, text: str) -> str:
        """
        Predict phrases in a text using the loaded model.

        Parameters
        ----------
        text: str
            The input text.
        
        Returns
        -------
        str
            The text where detected phrases are joined with underscores.
        """
        if self.model:
            tokens = tokenize(text)
            phrases = self.model[tokens]
            return " ".join(phrases)
        else:
            print("Model not loaded.")
            return ""