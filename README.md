# FORPY — Learn Python with AI

**Free and open-source Python learning app.**
Generate unlimited mini-exercises with AI, choose your level, and get instant corrections.

> Bring your own API key. No server. No subscription. Works 100% locally.

---

## Why FORPY?

Rather than grinding through a handful of long exercises, FORPY generates mini-exercises in seconds. In the time it takes to do 10 classic exercises, you can work through 80+ different exercises across all Python concepts — from beginner variables to expert architecture patterns.

---

## Demo
[![Watch the demo](miniature.jpg)](https://youtu.be/KWCZ96jlIlk)



## Features

- **6 progressive levels** — Noob → Débutant → Intermédiaire → Intermédiaire ++ → POO → Expert Architecture
- **25 specialised sub-levels** — classic exercises, debugging sessions, Pythonic rewrites, and design patterns
- **AI-powered generation** — every exercise is unique, never repeated back-to-back
- **4-part correction** — statement, Python code solution, line-by-line explanation, and oral walkthrough
- **Multi-provider** — Anthropic (Claude), OpenAI (GPT), Google (Gemini)
- **Multilingual** — interface and exercises independently configurable (English / French)
- **No server** — your API key stays on your device and is sent only to your chosen AI provider

---

## Download

| Platform | File |
|---|---|
| Windows | `forpy-v1.0.exe` |
| Linux | `forpy-v1.0.AppImage` |
| Android | `forpy-v1.0.apk` |

> Downloads are available on the [Releases](../../releases) page.

---

## Quick Start

1. Download and install the app for your platform
2. Launch **FORPY**
3. Open **Settings** (⚙ icon)
4. Select your AI provider and paste your API key
5. Choose a level and start learning

### Getting an API Key

| Provider | Link |
|---|---|
| Anthropic (Claude) | https://console.anthropic.com |
| OpenAI (GPT) | https://platform.openai.com |
| Google (Gemini) | https://aistudio.google.com |

---

## Build from Source

### Requirements

- Python 3.10+
- [Flutter SDK](https://flutter.dev/docs/get-started/install)

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run in development

```bash
python main.py
```

### Run tests

```bash
python -m pytest
```

### Package for distribution

```bash
# Windows (.exe)
python -m flet.cli build windows --project forpy --build-version 1.0.0

# Linux (.AppImage)
python -m flet.cli build linux --project forpy --build-version 1.0.0

# Android (.apk)
python -m flet.cli build apk --project forpy --build-version 1.0.0
```

> Packaging requires Flutter SDK. Run `flutter doctor` to verify your setup.

---

## Project Structure

```
forpy/
├── main.py                          # Entry point — Flet routing, theme init
├── pyproject.toml                   # Project config / dependencies
├── requirements.txt                 # pip dependencies
├── settings.example.json            # Config template (no API key)
│
├── screens/
│   ├── home_screen.py               # Home — logo, chapter buttons, settings link
│   ├── chapter_screen.py            # Chapter selection (Python, Python ML…)
│   ├── level_screen.py              # Level selection (6 levels)
│   ├── sublevel_screen.py           # Sub-level selection
│   ├── exercise_screen.py           # Exercise display (4 blocks + "Another exercise")
│   ├── pattern_screen.py            # Pattern selection — 2-column menu
│   ├── logic_screen.py              # "See the logic" image view per level
│   └── settings_screen.py          # API key, provider, languages, dark/light toggle
│
├── services/
│   ├── ai_service.py                # AI calls — Strategy pattern (Claude/OpenAI/Gemini/compatible)
│   └── prompt_builder.py           # Prompt loader + variable injection
│
├── prompts/python/                  # One .txt file per sub-level (25 files)
│   ├── noob.txt
│   ├── debutant.txt / debutant_plus.txt / debug_debutant.txt
│   ├── intermediaire.txt / intermediaire_avance.txt
│   ├── debug_intermediaire.txt / pythonique_intermediaire.txt / pattern_intermediaire.txt
│   ├── fonctions_avancees.txt / manipulation_structure.txt
│   ├── entree_sortie_erreurs.txt / organisation_code.txt
│   ├── debug_intermediaire_plus.txt / pythonique_intermediaire_plus.txt / pattern_intermediaire_plus.txt
│   ├── intro_poo.txt / poo_plus.txt / debug_poo.txt / poo_pythonique.txt / pattern_poo.txt
│   └── architecture.txt / debug_architecture.txt / architecture_pythonique.txt / pattern_expert.txt
│
├── utils/
│   ├── session_state.py             # Read/write settings.json — last topic, theme, pattern, languages
│   ├── theme.py                     # Dark/light palettes + UI style helpers
│   ├── translations.py             # Translation loader (reads translations.json)
│   └── translations.json           # All UI strings by language (EN, FR…)
│
├── assets/                          # Static resources
│   ├── icon.png / logo-forpy.png
│   ├── splash.png / splash-dark.png
│   └── logique_*.png                # "See the logic" diagrams per level
│
├── tests/
│   ├── conftest.py                  # Shared pytest fixtures
│   ├── test_ai_service.py
│   ├── test_prompt_builder.py
│   ├── test_session_state.py
│   └── test_translations.py
│
└── logs/
    ├── app.log                      # General logs
    ├── api_errors.log               # AI call errors
    └── json_errors.log              # JSON parsing errors
```

---

## Contributing

Contributions are welcome. The easiest way to contribute is to improve or add prompt files in `prompts/python/`. Each file:
- Must contain `{language}` (exercise language placeholder)
- Must contain `{last_topic}` (anti-repetition placeholder)
- Must produce a JSON response with exactly 4 keys: `enonce`, `correction`, `explication`, `deroulement`

See [CLAUDE.md](CLAUDE.md) for the full architecture documentation.

---

## License

[MIT](LICENSE) — © 2026 SylvainR-dev
