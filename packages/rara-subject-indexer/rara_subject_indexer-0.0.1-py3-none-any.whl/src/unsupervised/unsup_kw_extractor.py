import re

from estnltk import Text
from gensim.models.phrases import Phraser
from gensim.utils import tokenize
from langdetect import detect
from nltk.stem.snowball import SnowballStemmer
from rakun2 import RakunKeyphraseDetector
from src.unsupervised.spellcorrector import SpellCorrector
from src.utils.constants import (SUPPORTED_STOPWORDS, SUPPORTED_PHRASER_MODEL_PATHS, SUPPORTED_STEMMER_LANGUAGES,
                                 URL_REGEX, EMAIL_REGEX)


class KeywordExtractor:
    """
    A class for extracting keywords from the text using unsupervised extraction.
    """

    def __init__(self):
        """
        Initialize extractor using config provided in the constants file.
        """
        self.stopwords = SUPPORTED_STOPWORDS
        self.phraser_paths = SUPPORTED_PHRASER_MODEL_PATHS
        self.stemmer_languages = SUPPORTED_STEMMER_LANGUAGES
        self.url_pattern = URL_REGEX
        self.email_pattern = EMAIL_REGEX
        self.spell_corrector = SpellCorrector()

    def predict(self, text: str, lang_code: str = None, top_n: int = 10, merge_threshold: float = 0.0,
                use_phraser: bool = True, correct_spelling: bool = True, preserve_case: bool = True,
                max_uppercase: int = 2, min_word_frequency: int = 3) -> list[str]:
        """
        Extract keywords from the text using unsupervised extraction.

        Parameters
        ----------
        text: str
            Input text.
        lang_code: str, default None
            The language code of the input text.
        top_n: int, default 10
            Number of keywords to extract.
        merge_threshold: float, default 0.0
            Threshold for merging words into a single keyword.
        use_phraser: bool, default True
            Whether to use phraser or not.
        correct_spelling: bool, default True
            Whether to use spell correction or not.
        preserve_case: bool, default True
            Whether to preserve original case or not.
        max_uppercase: int, default 2
            The maximum number of uppercase letters in the word to allow spelling correction. If the word contains more
            than `max_uppercase` uppercase letters, it will not be corrected using spelling correction.
            This helps prevent corrections of words that are intentionally capitalized (like acronyms).
        min_word_frequency: int, default 2
            The minimum frequency of the word in the input text required for it to NOT be corrected. If the word
            appears fewer than `min_word_frequency` times in the `full_text`, it will be corrected using spelling
            correction. This helps prevent corrections of common words that are not likely to need correction.

        Returns
        -------
        keywords: list[str]
            List of keywords extracted from the input text.

        """
        if not lang_code:
            lang_code = detect(text)

        cleaned_text, places = self._clean_text_and_extract_places(text, lang_code)

        if correct_spelling:
            cleaned_text = self.spell_corrector.correct_text(
                    text=cleaned_text,
                    lang_code=lang_code,
                    max_uppercase=max_uppercase,
                    min_word_frequency=min_word_frequency,
                    preserve_case=preserve_case,
                    places=places
                )

        tokens = tokenize(cleaned_text)
        
        if use_phraser and lang_code in self.phraser_paths:
            tokens = self._apply_phraser(tokens, lang_code)

        processed_text = " ".join(tokens)
        keywords = self._extract_keywords(processed_text, lang_code, top_n, merge_threshold, preserve_case)

        # Remove duplicates
        keywords = list(dict.fromkeys(keywords))
        return keywords

    def _clean_text_and_extract_places(self, text: str, lang_code: str) -> tuple[str, set[str]]:
        """
        Clean the text using lemmatisation or stemming according to the input language and extract place names using
        NER if text is in Estonian. Also remove urls and email addresses using regex.

        Parameters
        ----------
        text: str
            Input text.
        lang_code: str
            The language code of the input text.

        Returns
        -------
        tuple[str, set[str]]
            The cleaned text and a set of extracted place names.
        """
        text = re.sub(self.url_pattern, "", text)
        text = re.sub(self.email_pattern, "", text)

        if lang_code == "et":
            return self._lemmatise_text_and_save_places(text)
        return self._stem_text(text, lang_code), set()

    def _lemmatise_text_and_save_places(self, text: str) -> tuple[str, set[str]]:
        """
        Lemmatise the text using EstNLTK package. Extract place names using NER.

        Parameters
        ----------
        text: str
            Input text.

        Returns
        -------
        tuple[str, set[str]]
            The cleaned text and a set of extracted place names.
        """
        layered_text = Text(text)
        layered_text.tag_layer(["morph_analysis", "ner"])
        human_names = {token.lemma[0] for entity in layered_text.ner if entity.nertag == "PER" for token in entity}
        places = {token.lemma[0] for entity in layered_text.ner if entity.nertag == "LOC" for token in entity}
        filtered_words = [token[0] for token, postag in zip(layered_text.lemma, layered_text.partofspeech) if
                          "V" not in postag and "A" not in postag and token[0] not in human_names]
        return " ".join(filtered_words), places

    def _stem_text(self, text: str, lang_code: str) -> str:
        """
        Apply stemming on the text.

        Parameters
        ----------
        text: str
            Input text.
        lang_code: str
            The language code of the input text.

        Returns
        -------
        text: str
            The stemmed text.
        """
        if lang_code in self.stemmer_languages:
            stemmer = SnowballStemmer(self.stemmer_languages[lang_code])
            return " ".join(stemmer.stem(word) for word in text.split())
        return text

    def _apply_phraser(self, tokens: list[str], lang_code: str) -> list[str]:
        """
        Apply phraser on the input text.

        Parameters
        ----------
        tokens: list[str]
            Input text as a list of tokens.
        lang_code: str
            The language code of the input text.

        Returns
        -------
        list[str]
            Tokens where found phrases are joined together using underscore.
        """
        phraser = Phraser.load(self.phraser_paths[lang_code])
        return phraser[tokens]

    def _extract_keywords(self, text: str, lang_code: str, top_n: int, merge_threshold: float,
                          preserve_case: bool) -> list[str]:
        """
        Run Rakun2 keyword extraction on the input text.

        Parameters
        ----------
        text: str
            Input text.
        lang_code: str
            The language code of the input text.
        top_n: int
            Number of keywords to extract.
        merge_threshold: float
            Threshold for merging words into a single keyword.
        preserve_case: bool
            Whether to preserve original case or not.

        Returns
        -------
        keywords: list[str]
            List of keywords extracted from the input text.
        """
        stopwords = self.stopwords.get(lang_code, [])
        detector = RakunKeyphraseDetector(
            {"num_keywords": top_n, "merge_threshold": merge_threshold, "stopwords": stopwords}, verbose=False, )
        keywords = [kw[0] for kw in detector.find_keywords(text, input_type="string")]

        if preserve_case:
            return self._match_original_case(text, keywords)
        return keywords

    def _match_original_case(self, text: str, keywords: list[str]) -> list[str]:
        """
        Match keywords to the original case.

        Parameters
        ----------
        text: str
            Input text.
        keywords: str
            List of keywords extracted from the input text.

        Returns
        -------
        original_cased_keywords: list[str]
            List of keywords extracted from the input text matched to the original case in the input text.
        """
        original_cased_keywords = []
        for keyword in keywords:
            pattern = rf'\b{re.escape(keyword)}\b'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                original_cased_keywords.append(match.group(0))
        return original_cased_keywords