import os
from stop_words import get_stop_words

from src.utils.path_helper import get_data_dir


def load_lines_from_file_to_list(file_path: str) -> list[str]:
    """
    Load lines from file into a list.

    Parameters
    ----------
    file_path : str
        Path to the file to load.

    Returns
    -------
    list[str]
        A list of strings.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]

# Stopwords for supported languages
SUPPORTED_STOPWORDS = {
    "en": get_stop_words("en"), 
    "et": load_lines_from_file_to_list(os.path.join(get_data_dir(), "estonian-stopwords-lemmas.txt")),
}

# Stopwords for supported languages used for phrase detection
SUPPORTED_STOPWORDS_PHRASER = {
    "en": get_stop_words("en"), 
    "et": load_lines_from_file_to_list(os.path.join(get_data_dir(), "estonian-stopwords.txt")),
}

# Supported Phraser model paths
SUPPORTED_PHRASER_MODEL_PATHS = {
    #"en": os.path.join(get_data_dir(), "models", "unsupervised", "model_name.model"),
    "et": os.path.join(get_data_dir(), "models", "unsupervised", "phraser_ise_digar_et.model"),
}

# Supported languages for using stemmer
SUPPORTED_STEMMER_LANGUAGES = {"en": "english"}

SENTENCE_SPLIT_REGEX = r"(?<!\d\.\d)(?<!\w\.\w)(?<=\.|\?|!)\s"

URL_REGEX = r"(?i)(https?://\S+|www\.\S+|doi(:|\.org/)\s*\S+)"

EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b"

# Spell check dictionary config
# Spell check will use default values term_index=0, count_index=1, separator=" unless redefined here
SPELL_CHECK_DICTIONARIES_CONFIG = {
    "et": {
        "path": os.path.join(get_data_dir(), "et_frequency_lemmas.txt"),
        "term_index": 1,
        "count_index": 0,
        "separator":" "
    },
    "en": {
        "path": os.path.join(get_data_dir(), "en_full.txt"),
    },
}