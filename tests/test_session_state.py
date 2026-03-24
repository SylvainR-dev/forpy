"""
Tests for utils/session_state.py

Covers:
- Default values on first run (no settings.json)
- Loading settings from a valid settings.json
- save_settings writes all 4 fields correctly
- Corrupt JSON falls back to defaults
- Missing file falls back to defaults
- set_sublevel resets last_exercise_topic on level change
- set_sublevel keeps last_exercise_topic on same level
- update_last_topic works
- Property setters update the internal dict
"""
import json
import os
import pytest
import utils.session_state as ss_module


@pytest.fixture
def tmp_settings(tmp_path, monkeypatch):
    """Redirect settings path to a temp file for each test."""
    path = str(tmp_path / "settings.json")
    monkeypatch.setattr(ss_module, "_get_settings_path", lambda: path)
    return path


def make_session(tmp_settings):
    """Create a fresh SessionState with the temp settings path active."""
    from utils.session_state import SessionState
    return SessionState()


class TestDefaults:
    def test_no_settings_file_uses_defaults(self, tmp_settings):
        s = make_session(tmp_settings)
        assert s.api_key == ""
        assert s.provider == "anthropic"
        assert s.interface_language == "english"
        assert s.exercise_language == "english"

    def test_default_runtime_state(self, tmp_settings):
        s = make_session(tmp_settings)
        assert s.current_chapter == "python"
        assert s.current_level == ""
        assert s.current_sublevel == ""
        assert s.last_exercise_topic == ""


class TestLoadSettings:
    def test_loads_all_four_fields(self, tmp_settings):
        data = {
            "api_key": "sk-abc",
            "provider": "openai",
            "interface_language": "french",
            "exercise_language": "french",
        }
        with open(tmp_settings, "w") as f:
            json.dump(data, f)

        s = make_session(tmp_settings)
        assert s.api_key == "sk-abc"
        assert s.provider == "openai"
        assert s.interface_language == "french"
        assert s.exercise_language == "french"

    def test_partial_file_uses_defaults_for_missing_keys(self, tmp_settings):
        with open(tmp_settings, "w") as f:
            json.dump({"api_key": "sk-partial"}, f)

        s = make_session(tmp_settings)
        assert s.api_key == "sk-partial"
        assert s.provider == "anthropic"  # default

    def test_corrupt_json_falls_back_to_defaults(self, tmp_settings):
        with open(tmp_settings, "w") as f:
            f.write("not valid json {{{")

        s = make_session(tmp_settings)
        assert s.api_key == ""
        assert s.provider == "anthropic"

    def test_empty_file_falls_back_to_defaults(self, tmp_settings):
        with open(tmp_settings, "w") as f:
            f.write("")

        s = make_session(tmp_settings)
        assert s.api_key == ""


class TestSaveSettings:
    def test_save_writes_all_four_fields(self, tmp_settings):
        s = make_session(tmp_settings)
        s.api_key = "sk-save"
        s.provider = "gemini"
        s.interface_language = "french"
        s.exercise_language = "english"
        s.save_settings()

        with open(tmp_settings) as f:
            saved = json.load(f)

        assert saved["api_key"] == "sk-save"
        assert saved["provider"] == "gemini"
        assert saved["interface_language"] == "french"
        assert saved["exercise_language"] == "english"

    def test_save_then_reload_roundtrip(self, tmp_settings):
        s1 = make_session(tmp_settings)
        s1.api_key = "sk-roundtrip"
        s1.provider = "openai"
        s1.save_settings()

        s2 = make_session(tmp_settings)
        assert s2.api_key == "sk-roundtrip"
        assert s2.provider == "openai"

    def test_api_key_never_saved_to_git(self, tmp_settings):
        """settings.json must be in .gitignore."""
        gitignore = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            ".gitignore",
        )
        with open(gitignore) as f:
            content = f.read()
        assert "settings.json" in content


class TestPropertySetters:
    def test_api_key_setter(self, tmp_settings):
        s = make_session(tmp_settings)
        s.api_key = "new-key"
        assert s.api_key == "new-key"

    def test_provider_setter(self, tmp_settings):
        s = make_session(tmp_settings)
        s.provider = "gemini"
        assert s.provider == "gemini"

    def test_interface_language_setter(self, tmp_settings):
        s = make_session(tmp_settings)
        s.interface_language = "french"
        assert s.interface_language == "french"

    def test_exercise_language_setter(self, tmp_settings):
        s = make_session(tmp_settings)
        s.exercise_language = "french"
        assert s.exercise_language == "french"


class TestSetSublevel:
    def test_set_sublevel_resets_topic_on_change(self, tmp_settings):
        s = make_session(tmp_settings)
        s.current_sublevel = "debutant"
        s.last_exercise_topic = "boucles"

        s.set_sublevel("Débutant", "debutant_plus")  # different sublevel
        assert s.last_exercise_topic == ""

    def test_set_sublevel_keeps_topic_on_same_sublevel(self, tmp_settings):
        s = make_session(tmp_settings)
        s.current_sublevel = "debutant"
        s.last_exercise_topic = "listes"

        s.set_sublevel("Débutant", "debutant")  # same sublevel
        assert s.last_exercise_topic == "listes"

    def test_set_sublevel_updates_level_and_sublevel(self, tmp_settings):
        s = make_session(tmp_settings)
        s.set_sublevel("Intermédiaire", "intermediaire_avance")
        assert s.current_level == "Intermédiaire"
        assert s.current_sublevel == "intermediaire_avance"


class TestUpdateLastTopic:
    def test_update_last_topic(self, tmp_settings):
        s = make_session(tmp_settings)
        s.update_last_topic("variables et types")
        assert s.last_exercise_topic == "variables et types"

    def test_update_last_topic_overrides_previous(self, tmp_settings):
        s = make_session(tmp_settings)
        s.update_last_topic("listes")
        s.update_last_topic("dictionnaires")
        assert s.last_exercise_topic == "dictionnaires"
