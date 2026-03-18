import json
import os

_TRANSLATIONS_PATH = os.path.join(os.path.dirname(__file__), "translations.json")
_cache: dict = {}


def get_translations(language) -> dict:
    """Return the translation dict for the given language.
    Falls back to English if the language is not found or is falsy.
    """
    global _cache
    if not _cache:
        with open(_TRANSLATIONS_PATH, encoding="utf-8") as f:
            _cache = json.load(f)
    return _cache.get(language or "english", _cache["english"])
