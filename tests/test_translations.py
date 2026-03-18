"""
Tests for utils/translations.py and utils/translations.json

Covers:
- All required UI keys present in every supported language
- All error keys map correctly (error_<ValueError_key>)
- Unknown language falls back to english
- Translation cache is shared (same object returned)
- No language has empty string values for required keys
"""
import pytest
from utils.translations import get_translations

SUPPORTED_LANGUAGES = ["english", "french"]

# Keys used in screens — must exist in every language
REQUIRED_KEYS = [
    "welcome",
    "settings",
    "api_key",
    "provider",
    "another_exercise",
    "level",
    "sublevel",
    "interface_language",
    "exercise_language",
    "choose_level",
    "choose_sublevel",
    "statement",
    "correction",
    "explanation",
    "walkthrough",
    "generating",
    "back",
    "save",
    "settings_saved",
    "chapter_python",
    # Error keys — must match ValueError keys raised by ai_service
    "error_no_api_key",
    "error_invalid_key",
    "error_quota",
    "error_timeout",
    "error_json",
    "error_generic",
]

# ValueError keys raised by ai_service.py → must map to a translation key
VALUEERROR_KEYS = ["no_api_key", "invalid_key", "quota", "timeout", "json", "generic"]


class TestRequiredKeys:
    @pytest.mark.parametrize("lang", SUPPORTED_LANGUAGES)
    def test_all_required_keys_present(self, lang):
        t = get_translations(lang)
        missing = [k for k in REQUIRED_KEYS if k not in t]
        assert not missing, f"[{lang}] Missing keys: {missing}"

    @pytest.mark.parametrize("lang", SUPPORTED_LANGUAGES)
    def test_no_empty_string_values(self, lang):
        t = get_translations(lang)
        empty = [k for k in REQUIRED_KEYS if t.get(k, "") == ""]
        assert not empty, f"[{lang}] Empty string values for: {empty}"

    @pytest.mark.parametrize("lang", SUPPORTED_LANGUAGES)
    def test_all_valueerror_keys_map_to_translation(self, lang):
        """exercise_screen uses t.get('error_<key>') — every key must exist."""
        t = get_translations(lang)
        for key in VALUEERROR_KEYS:
            translation_key = f"error_{key}"
            assert translation_key in t, (
                f"[{lang}] Translation missing for ValueError('{key}'): "
                f"need key '{translation_key}'"
            )


class TestFallback:
    def test_unknown_language_falls_back_to_english(self):
        unknown = get_translations("klingon")
        english = get_translations("english")
        assert unknown == english

    def test_none_language_falls_back_to_english(self):
        result = get_translations(None)
        english = get_translations("english")
        assert result == english

    def test_empty_string_language_falls_back_to_english(self):
        result = get_translations("")
        english = get_translations("english")
        assert result == english


class TestLanguageContent:
    def test_english_and_french_differ(self):
        """Sanity check: languages must not be identical."""
        en = get_translations("english")
        fr = get_translations("french")
        assert en["welcome"] != fr["welcome"]
        assert en["settings"] != fr["settings"]

    def test_english_welcome_message(self):
        assert get_translations("english")["welcome"] == "Welcome to FORPY"

    def test_french_welcome_message(self):
        assert get_translations("french")["welcome"] == "Bienvenue sur FORPY"

    def test_cache_returns_same_object(self):
        """Calling get_translations twice should return the same dict (cached)."""
        t1 = get_translations("english")
        t2 = get_translations("english")
        assert t1 is t2
