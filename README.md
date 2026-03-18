# FORPY — Learn Python with AI

**Free and open-source Python learning app.**
Generate unlimited mini-exercises with AI, choose your level, and get instant corrections.

> Bring your own API key. No server. No subscription. Works 100% locally.

---

## Why FORPY?

Rather than grinding through a handful of long exercises, FORPY generates mini-exercises in seconds. In the time it takes to do 10 classic exercises, you can work through 80+ different exercises across all Python concepts — from beginner variables to expert architecture patterns.

---

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
├── main.py               # Entry point
├── screens/              # UI screens (home, level, sublevel, exercise, settings)
├── services/             # AI provider abstraction + prompt builder
├── prompts/python/       # 25 prompt files, one per sub-level
├── utils/                # Session state, translations
└── logs/                 # Local error logs (api_errors, json_errors, app)
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
