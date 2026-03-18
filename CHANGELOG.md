# Changelog

All notable changes to FORPY are documented in this file.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

---

## [1.0.0] — 2026-03-18

### Added

**Core**
- `main.py` — Flet app entry point with stacked view navigation and physical back-button support
- `utils/session_state.py` — Runtime navigation state + persistent settings (api_key, provider, languages)
- `utils/translations.json` — Full UI translation for English and French
- `utils/translations.py` — Translation loader with caching and English fallback

**AI Service**
- `services/ai_service.py` — Strategy pattern with three providers: Claude (Anthropic), GPT (OpenAI), Gemini (Google)
- Automatic retry (×2) on timeout and JSON parse errors
- Immediate raise on invalid API key and quota errors
- Per-provider exception mapping to user-friendly `ValueError` keys
- File-based logging to `logs/api_errors.log` and `logs/json_errors.log`

**Prompt Builder**
- `services/prompt_builder.py` — Loads the correct `.txt` prompt file by chapter + sub-level
- Injects `{language}` (exercise language) and `{last_topic}` (anti-repetition) into every prompt

**Screens**
- `home_screen.py` — Welcome screen with Python chapter button and Settings shortcut
- `level_screen.py` — 6-level selector with full sub-level mapping
- `sublevel_screen.py` — Sub-level selector for the chosen level
- `exercise_screen.py` — Async exercise generation with loading indicator, 4-section display, and "Another exercise" button
- `settings_screen.py` — API key, AI provider selection, interface language, exercise language with live save
- `chapter_screen.py` — Chapter stub (Python MVP, extensible for future chapters)

**Prompts** — 25 prompt files covering all sub-levels:
- Noob (1), Débutant (3), Intermédiaire (5), Intermédiaire ++ (7), POO (5), Expert Architecture (4)
- Each prompt enforces the universal JSON output format: `enonce`, `correction`, `explication`, `deroulement`

**Tests**
- `tests/test_ai_service.py` — 17 tests: JSON parser (9 cases), provider factory (5), retry logic (8)
- `tests/test_prompt_builder.py` — 13 tests: language injection, last_topic injection, file existence
- `tests/test_session_state.py` — 18 tests: defaults, load, save, roundtrip, property setters, sublevel reset
- `tests/test_translations.py` — 12 tests: required keys, fallback, empty values, cache

**Project config**
- `pyproject.toml` — Pytest config (`asyncio_mode = auto`) + Flet build metadata
- `requirements.txt` — Runtime dependencies
- `settings.example.json` — Template for user settings (committed; `settings.json` is gitignored)
- `CLAUDE.md` — Full architecture documentation for contributors and AI assistants

### Security
- `settings.json` added to `.gitignore` — API key never committed to the repository

---

## [Unreleased]

Planned for future releases:
- macOS and iOS packaging
- Additional language support (Spanish, German, …)
- New chapters: Python ML, Python IA
- Progress tracking per sub-level
- Dark / light theme toggle
