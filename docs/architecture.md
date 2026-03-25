# FORPY — Architecture

## Overview

FORPY (For Python) is an open source, AI-powered Python learning app built with [Flet](https://flet.dev/) — a single Python codebase that runs natively on Windows, Linux, and Android.

The core architectural decision is **prompt-driven content generation**: instead of maintaining a static database of exercises, FORPY externalizes content entirely to the AI. Each exercise is generated on demand via the user's own AI provider API key, stored locally on their device. No backend, no server, no subscription.

---

## Architectural Philosophy

### Prompt-Driven vs. Database-Driven

Most learning apps store hundreds of static exercises in a database. FORPY takes the opposite approach:

| Traditional approach | FORPY approach |
|---|---|
| Static exercise database | Zero stored exercises |
| Backend server required | 100% local, no server |
| Fixed content, limited variety | Infinite variety, never repeats |
| Maintenance cost (content updates) | Zero content maintenance |
| User data on remote servers | User data stays on device |

The **prompt IS the database**. Each of the 25 sub-levels has a dedicated `.txt` prompt file, carefully crafted to generate consistent, pedagogically sound exercises. The AI handles content generation; FORPY handles structure, delivery, and user experience.

### No Sandbox by Design

FORPY deliberately does not include a code execution sandbox. The app is a **content generator**, not an IDE. Users write and run their code in their own editor (VS Code or other). This decision eliminates an entire class of security vulnerabilities — arbitrary code execution, resource exhaustion, sandboxing bypasses — while keeping the app simple, lightweight, and auditable.

### Local API Key Storage

The user provides their own AI provider API key (Anthropic, OpenAI, Gemini, or any OpenAI-compatible provider). The key is stored exclusively in a local `settings.json` file on the user's device, which is excluded from the repository via `.gitignore`. No key ever transits through any FORPY infrastructure — because there is none.

---

## Global Architecture

```
User
 │
 ▼
Flet App (local, no server)
 │
 ├── Choose Chapter (Python — extensible: Python ML, Python AI...)
 │
 ├── Choose Level (6 levels: Noob → Expert Architecture)
 │
 ├── Choose Sub-Level (25 sub-levels total)
 │        │
 │        ├── [See the Logic] → Visual summary of the level's key principles
 │        │
 │        └── [Pattern] → 2-column pattern selector (from Intermediate onwards)
 │
 ▼
PromptFactory loads the corresponding .txt prompt
 │
 ▼
Variable injection: {language}, {last_topic}, {category}, {pattern}
 │
 ▼
AIService sends prompt to the selected AI provider
(Strategy Pattern: Claude / OpenAI / Gemini / OpenAI-compatible)
 │
 ▼
JSON response parsed (universal 4-field format)
 │
 ▼
Exercise displayed:
  ├── 📝 Statement
  ├── ✅ Correction (Python code, monospace)
  ├── 💡 Line-by-line explanation
  └── 🎙 Oral walkthrough
 │
 ▼
[Another Exercise] → re-injects last topic to avoid repetition
```

---

## Project Structure

```
forpy/
├── main.py                   # Entry point — Flet routing, theme init
├── pyproject.toml            # Project config and dependencies
├── requirements.txt          # pip dependencies
├── settings.example.json     # Config template (no API key)
│
├── screens/
│   ├── home_screen.py        # Home — logo, chapter buttons, settings link
│   ├── chapter_screen.py     # Chapter selection
│   ├── level_screen.py       # Level selection (6 levels)
│   ├── sublevel_screen.py    # Sub-level selection
│   ├── exercise_screen.py    # Exercise display (4 blocks + "Another exercise")
│   ├── pattern_screen.py     # Pattern selector — 2-column menu
│   ├── logic_screen.py       # "See the logic" visual per level
│   └── settings_screen.py    # API key, provider, languages, dark/light toggle
│
├── services/
│   ├── ai_service.py         # AI calls — Strategy Pattern (Claude/OpenAI/Gemini)
│   └── prompt_builder.py     # Prompt loader + variable injection
│
├── prompts/python/           # 25 prompt files, one per sub-level
│   ├── noob.txt
│   ├── debutant.txt
│   ├── ...
│   └── pattern_expert.txt
│
├── utils/
│   ├── session_state.py      # Read/write settings.json — last topic, theme, languages
│   ├── theme.py              # Dark/light palettes and UI style helpers
│   ├── translations.py       # Translation loader
│   └── translations.json     # All UI strings by language (EN, FR)
│
├── assets/                   # Static resources — icons, splash, logic diagrams
│
├── tests/
│   ├── test_ai_service.py
│   ├── test_prompt_builder.py
│   ├── test_session_state.py
│   └── test_translations.py
│
└── logs/
    ├── app.log
    ├── api_errors.log
    └── json_errors.log
```

---

## Design Patterns

### Strategy Pattern — AI Providers

Multiple AI providers are supported through a common interface. Adding a new provider requires implementing a single `call()` method — no changes to the rest of the app.

```python
class AIProvider:
    def call(self, prompt: str, api_key: str) -> str:
        raise NotImplementedError

class ClaudeProvider(AIProvider):
    def call(self, prompt, api_key): ...   # Anthropic API

class OpenAIProvider(AIProvider):
    def call(self, prompt, api_key): ...   # OpenAI API

class GeminiProvider(AIProvider):
    def call(self, prompt, api_key): ...   # Google Gemini API
```

### Factory Pattern — Prompt Selection

The `PromptFactory` resolves the correct prompt file from the `Chapter + SubLevel` combination and injects runtime variables before sending to the AI.

```python
class PromptFactory:
    def get_prompt(self, chapter, sublevel, language,
                   last_topic="", category="", pattern=""):
        path = f"prompts/{chapter}/{sublevel}.txt"
        prompt = open(path).read()
        prompt = prompt.replace("{language}", language)
        prompt = prompt.replace("{last_topic}", last_topic)
        prompt = prompt.replace("{category}", category)
        prompt = prompt.replace("{pattern}", pattern)
        return prompt
```

---

## Data Model

### Universal Exercise Format (JSON)

All AI responses — regardless of sub-level type (standard, debug, pythonic, pattern) — conform to a single JSON structure:

```json
{
  "enonce":      "Clear, simple statement of the exercise",
  "correction":  "Complete Python solution, ready to copy",
  "explication": "Line-by-line explanation, no jargon",
  "deroulement": "Fluent oral description of how the code runs"
}
```

### Session State

Persisted locally in `settings.json`:

```json
{
  "api_key": "...",
  "provider": "anthropic",
  "interface_language": "english",
  "exercise_language": "english",
  "theme": "dark",
  "last_exercise_topic": "lists",
  "last_sublevel": "debutant",
  "current_pattern_category": "",
  "current_pattern": ""
}
```

`last_exercise_topic` is re-injected into the next prompt as a constraint, ensuring the AI never generates the same exercise twice in a row.

---

## Pedagogical Structure

FORPY's learning path is structured around 6 progressive levels, each with dedicated sub-levels targeting specific learning dimensions:

| Level | Sub-levels | Focus |
|---|---|---|
| Noob | Noob | First contact with Python syntax |
| Beginner | Beginner, Beginner++, Debug | Core constructs + reading broken code |
| Intermediate | Standard, Advanced, Debug, Pythonic, Pattern | Idiomatic Python + design patterns |
| Intermediate++ | 7 sub-levels | Advanced functions, I/O, code organisation |
| OOP | Intro, OOP++, Debug, Pythonic, Pattern | Object-oriented thinking |
| Expert Architecture | Architecture, Debug, Pythonic, Pattern | Design patterns + clean architecture |

### "See the Logic" Feature

Each level includes a visual summary screen that communicates the **mental model** of that level before the user starts generating exercises. For example, the OOP level presents four guiding principles: encapsulate data, bind methods to data, define clear responsibilities, abstract complexity. This gives users a conceptual anchor, not just syntax to memorise.

### Pattern Selector (Intermediate and above)

From the Intermediate level onwards, a dedicated pattern screen presents a **2-column menu** — category on the left, specific patterns on the right — allowing users to target a precise language construct or design pattern. The selected `{category}` and `{pattern}` are injected directly into the prompt, producing a focused exercise on exactly that topic.

---

## Internationalisation

All UI strings are loaded from `utils/translations.json`. No hardcoded text exists anywhere in the codebase. Language changes are applied in real time without restarting the app. The exercise language is independent from the interface language — a user can navigate the UI in French while receiving exercises in English.

---

## Security Considerations

- `settings.json` is listed in `.gitignore` — API keys are never committed to the repository
- `settings.example.json` is provided as a documented template with no real key
- No API key is ever sent to any server other than the user's chosen AI provider
- No code execution environment is exposed to the user
- All data remains on the user's local device

---

## Extensibility

The architecture is designed to grow without refactoring:

- **New chapters** (Python ML, Python AI): add a folder under `prompts/` and register in `chapter_screen.py`
- **New sub-levels**: add a `.txt` prompt file and register in `sublevel_screen.py`
- **New AI providers**: implement `AIProvider.call()` and register in `ai_service.py`
- **New languages**: add a key block in `translations.json`
- **New pattern categories**: add entries to the `PATTERNS_*` dictionaries in `pattern_screen.py`