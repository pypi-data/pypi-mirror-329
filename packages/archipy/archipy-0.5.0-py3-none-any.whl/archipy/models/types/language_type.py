from enum import Enum


class LanguageType(str, Enum):
    """Enum representing supported languages for error messages."""

    FA = "fa"  # Persian
    EN = "en"  # English
