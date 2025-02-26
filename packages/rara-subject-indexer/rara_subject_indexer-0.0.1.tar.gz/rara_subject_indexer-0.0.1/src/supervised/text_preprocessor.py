from estnltk import Text
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

class TextPreprocessor:
    """
    A text preprocessor that performs optional language detection,
    and uses Estnltk for Estonian
    """

    def __init__(self, language: str):
        """
        Parameters
        ----------
        language : str, optional
            The default language to assume if detection fails, by default "en"
        """
        self.language = language
        self.stemmer = SnowballStemmer("english")

    def preprocess(self, text: str) -> str:
        """
        Detect language and lemmatize accordingly.

        Parameters
        ----------
        text : str
            The raw text to preprocess.

        Returns
        -------
        str
            The lemmatized text.
        """
        if not text:
            return ""
        if self.language == "et":
            et_text = Text(text).tag_layer()
            preprocessed_text = " ".join(token[0] for token in et_text.lemma)
        elif self.language == "en":
            preprocessed_text = " ".join(self.stemmer.stem(token) for token in word_tokenize(text))
        elif self.language is None:
            raise ValueError("Preprocessing language not set. Please set the language.")
        else:
            raise ValueError(f"Unsupported language: {self.language}."
                             f"Before using this language, add preprocessing logic.")

        return preprocessed_text
