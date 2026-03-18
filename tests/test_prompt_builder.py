"""
Tests for services/prompt_builder.py

Covers:
- {language} placeholder injection
- {last_topic} placeholder injection (with and without a topic)
- FileNotFoundError on missing prompt file
- All 25 prompt files load without error
- No raw placeholder left in the returned prompt
"""
import os
import pytest
from services.prompt_builder import PromptBuilder, PROMPTS_DIR

# Full mapping of level → sublevels from the architecture
ALL_SUBLEVEL_KEYS = [
    "noob",
    "debutant", "debutant_plus", "debug_debutant",
    "intermediaire", "intermediaire_avance", "debug_intermediaire",
    "pythonique_intermediaire", "pattern_intermediaire",
    "fonctions_avancees", "manipulation_structure", "entree_sortie_erreurs",
    "organisation_code", "debug_intermediaire_plus",
    "pythonique_intermediaire_plus", "pattern_intermediaire_plus",
    "intro_poo", "poo_plus", "debug_poo", "poo_pythonique", "pattern_poo",
    "architecture", "debug_architecture", "architecture_pythonique",
    "pattern_expert",
]


@pytest.fixture
def builder():
    return PromptBuilder()


class TestLanguageInjection:
    def test_language_placeholder_replaced(self, builder):
        prompt = builder.get_prompt("python", "noob", "french")
        assert "{language}" not in prompt
        assert "french" in prompt

    def test_english_language_injected(self, builder):
        prompt = builder.get_prompt("python", "debutant", "english")
        assert "english" in prompt
        assert "{language}" not in prompt

    def test_language_appears_in_every_prompt(self, builder):
        for key in ALL_SUBLEVEL_KEYS:
            prompt = builder.get_prompt("python", key, "english")
            assert "{language}" not in prompt, f"{{language}} not replaced in {key}.txt"


class TestLastTopicInjection:
    def test_last_topic_injected_when_provided(self, builder):
        prompt = builder.get_prompt("python", "noob", "english", last_topic="variables")
        assert "{last_topic}" not in prompt
        assert "variables" in prompt

    def test_last_topic_empty_leaves_no_placeholder(self, builder):
        prompt = builder.get_prompt("python", "debutant", "english", last_topic="")
        assert "{last_topic}" not in prompt

    def test_last_topic_default_is_empty(self, builder):
        prompt = builder.get_prompt("python", "noob", "english")
        assert "{last_topic}" not in prompt

    def test_last_topic_in_every_prompt(self, builder):
        for key in ALL_SUBLEVEL_KEYS:
            prompt = builder.get_prompt("python", key, "english", last_topic="boucles")
            assert "{last_topic}" not in prompt, f"{{last_topic}} not replaced in {key}.txt"
            assert "boucles" in prompt, f"last_topic not injected in {key}.txt"


class TestFileHandling:
    def test_missing_sublevel_raises_file_not_found(self, builder):
        with pytest.raises(FileNotFoundError):
            builder.get_prompt("python", "does_not_exist", "english")

    def test_missing_chapter_raises_file_not_found(self, builder):
        with pytest.raises(FileNotFoundError):
            builder.get_prompt("nonexistent_chapter", "noob", "english")

    def test_all_prompt_files_exist(self):
        for key in ALL_SUBLEVEL_KEYS:
            path = os.path.join(PROMPTS_DIR, "python", f"{key}.txt")
            assert os.path.isfile(path), f"Missing prompt file: {key}.txt"

    def test_all_prompt_files_are_non_empty(self):
        for key in ALL_SUBLEVEL_KEYS:
            path = os.path.join(PROMPTS_DIR, "python", f"{key}.txt")
            with open(path, encoding="utf-8") as f:
                content = f.read().strip()
            assert content, f"Prompt file is empty: {key}.txt"

    def test_prompt_returns_string(self, builder):
        result = builder.get_prompt("python", "noob", "english")
        assert isinstance(result, str)
        assert len(result) > 50  # sanity check for non-trivial content
