"""
AI provider abstraction — Strategy pattern.

Each provider implements `_call_once(prompt, api_key) -> dict`.
The base class `call_async` wraps it with:
  - asyncio timeout (CALL_TIMEOUT seconds)
  - automatic retry up to MAX_RETRIES times for timeout and JSON errors
  - immediate raise for invalid_key and quota errors (no retry)

ValueError keys raised (mapped to translations by exercise_screen):
    "no_api_key"   — API key not set
    "invalid_key"  — 401 / authentication error
    "quota"        — 429 / rate limit / quota exceeded
    "timeout"      — asyncio timeout or connection timeout
    "json"         — AI response could not be parsed as valid JSON
"""

import asyncio
import json
import logging
import os
import re
from logging.handlers import RotatingFileHandler

# ---------------------------------------------------------------------------
# File-based logging
# ---------------------------------------------------------------------------

_LOG_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "logs"))


def _file_logger(name: str, filename: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        os.makedirs(_LOG_DIR, exist_ok=True)
        handler = RotatingFileHandler(
            os.path.join(_LOG_DIR, filename),
            maxBytes=1_000_000,
            backupCount=3,
            encoding="utf-8",
        )
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)
    return logger


api_logger = _file_logger("forpy.api", "api_errors.log")
json_logger = _file_logger("forpy.json", "json_errors.log")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CALL_TIMEOUT = 60   # seconds per attempt
MAX_RETRIES = 3     # max attempts for timeout and JSON errors

# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------

_RETRYABLE_KEYS = {"timeout", "json"}


class AIProvider:
    """
    Base provider. Subclasses implement `_call_once`.
    Consumers call `call_async`, which handles timeout and retry.
    """

    async def _call_once(self, prompt: str, api_key: str, sublevel: str = "") -> dict:
        """Single raw API call. Must be overridden.
        Convert all SDK-specific errors to ValueError with a key:
            invalid_key | quota | timeout | json
        """
        raise NotImplementedError

    async def call_async(self, prompt: str, api_key: str, sublevel: str = "") -> dict:
        """Public entry point — adds timeout wrapper and retry logic."""
        last_exc: Exception = RuntimeError("Unknown error")

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                return await asyncio.wait_for(
                    self._call_once(prompt, api_key, sublevel),
                    timeout=CALL_TIMEOUT,
                )

            except asyncio.TimeoutError:
                api_logger.warning(
                    "[%s] Timeout on attempt %d/%d",
                    type(self).__name__, attempt, MAX_RETRIES,
                )
                last_exc = ValueError("timeout")

            except ValueError as exc:
                key = str(exc)
                if key in _RETRYABLE_KEYS:
                    if key == "json":
                        json_logger.warning(
                            "[%s] JSON parse error on attempt %d/%d",
                            type(self).__name__, attempt, MAX_RETRIES,
                        )
                    else:
                        api_logger.warning(
                            "[%s] Retryable error '%s' on attempt %d/%d",
                            type(self).__name__, key, attempt, MAX_RETRIES,
                        )
                    last_exc = exc
                else:
                    # invalid_key, quota — not retryable
                    raise

            except Exception as exc:
                api_logger.error(
                    "[%s] Unexpected error: %s", type(self).__name__, exc
                )
                raise

        raise last_exc


# ---------------------------------------------------------------------------
# Claude (Anthropic)
# ---------------------------------------------------------------------------

class ClaudeProvider(AIProvider):
    MODEL = "claude-haiku-4-5-20251001"

    async def _call_once(self, prompt: str, api_key: str, sublevel: str = "") -> dict:
        import anthropic

        client = anthropic.AsyncAnthropic(api_key=api_key)
        try:
            message = await client.messages.create(
                model=self.MODEL,
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}],
            )
        except anthropic.AuthenticationError:
            api_logger.warning("[ClaudeProvider] Invalid API key")
            raise ValueError("invalid_key")
        except anthropic.RateLimitError:
            api_logger.warning("[ClaudeProvider] Rate limit / quota exceeded")
            raise ValueError("quota")
        except anthropic.APITimeoutError:
            api_logger.warning("[ClaudeProvider] SDK-level timeout")
            raise ValueError("timeout")
        except anthropic.APIConnectionError as exc:
            api_logger.error("[ClaudeProvider] Connection error: %s", exc)
            raise ValueError("timeout")
        except anthropic.APIStatusError as exc:
            api_logger.error(
                "[ClaudeProvider] API error %d: %s", exc.status_code, exc.message
            )
            raise

        return _parse_json(message.content[0].text, sublevel)


# ---------------------------------------------------------------------------
# OpenAI
# ---------------------------------------------------------------------------

class OpenAIProvider(AIProvider):
    MODEL = "gpt-4o-mini"

    async def _call_once(self, prompt: str, api_key: str, sublevel: str = "") -> dict:
        import openai

        client = openai.AsyncOpenAI(api_key=api_key)
        try:
            response = await client.chat.completions.create(
                model=self.MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000,
            )
        except openai.AuthenticationError:
            api_logger.warning("[OpenAIProvider] Invalid API key")
            raise ValueError("invalid_key")
        except openai.RateLimitError:
            api_logger.warning("[OpenAIProvider] Rate limit / quota exceeded")
            raise ValueError("quota")
        except openai.APITimeoutError:
            api_logger.warning("[OpenAIProvider] SDK-level timeout")
            raise ValueError("timeout")
        except openai.APIConnectionError as exc:
            api_logger.error("[OpenAIProvider] Connection error: %s", exc)
            raise ValueError("timeout")
        except openai.APIStatusError as exc:
            api_logger.error(
                "[OpenAIProvider] API error %d: %s", exc.status_code, exc.message
            )
            raise

        return _parse_json(response.choices[0].message.content, sublevel)


# ---------------------------------------------------------------------------
# Gemini (Google)
# ---------------------------------------------------------------------------

class GeminiProvider(AIProvider):
    MODEL = "gemini-1.5-flash"

    async def _call_once(self, prompt: str, api_key: str, sublevel: str = "") -> dict:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(self.MODEL)

        try:
            # generate_content_async is the native async method
            response = await model.generate_content_async(prompt)
        except Exception as exc:
            # Map google-api-core errors by class name (avoids hard import)
            exc_name = type(exc).__name__
            exc_str = str(exc).lower()

            if exc_name in ("PermissionDenied", "Unauthenticated") or "api_key" in exc_str or "invalid" in exc_str:
                api_logger.warning("[GeminiProvider] Invalid API key: %s", exc)
                raise ValueError("invalid_key")
            if exc_name == "ResourceExhausted" or "quota" in exc_str or "429" in exc_str:
                api_logger.warning("[GeminiProvider] Quota exceeded: %s", exc)
                raise ValueError("quota")
            if exc_name == "DeadlineExceeded" or "deadline" in exc_str or "timeout" in exc_str:
                api_logger.warning("[GeminiProvider] Timeout: %s", exc)
                raise ValueError("timeout")

            api_logger.error("[GeminiProvider] Unexpected error: %s", exc)
            raise

        return _parse_json(response.text, sublevel)


# ---------------------------------------------------------------------------
# Grok (xAI) — OpenAI-compatible
# ---------------------------------------------------------------------------

class GrokProvider(AIProvider):
    MODEL = "grok-3"
    BASE_URL = "https://api.x.ai/v1"

    async def _call_once(self, prompt: str, api_key: str, sublevel: str = "") -> dict:
        import openai

        client = openai.AsyncOpenAI(api_key=api_key, base_url=self.BASE_URL)
        try:
            response = await client.chat.completions.create(
                model=self.MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000,
            )
        except openai.AuthenticationError:
            api_logger.warning("[GrokProvider] Invalid API key")
            raise ValueError("invalid_key")
        except openai.RateLimitError:
            api_logger.warning("[GrokProvider] Rate limit / quota exceeded")
            raise ValueError("quota")
        except openai.APITimeoutError:
            api_logger.warning("[GrokProvider] SDK-level timeout")
            raise ValueError("timeout")
        except openai.APIConnectionError as exc:
            api_logger.error("[GrokProvider] Connection error: %s", exc)
            raise ValueError("timeout")
        except openai.APIStatusError as exc:
            api_logger.error(
                "[GrokProvider] API error %d: %s", exc.status_code, exc.message
            )
            raise

        return _parse_json(response.choices[0].message.content, sublevel)


# ---------------------------------------------------------------------------
# LLaMA (Meta) — via Ollama (local) or any OpenAI-compatible endpoint
# ---------------------------------------------------------------------------

class LlamaProvider(AIProvider):
    MODEL = "llama3.2"
    BASE_URL = "http://localhost:11434/v1"

    async def _call_once(self, prompt: str, api_key: str, sublevel: str = "") -> dict:
        import openai

        # Ollama accepts any non-empty string as api_key
        effective_key = api_key if api_key else "ollama"
        client = openai.AsyncOpenAI(api_key=effective_key, base_url=self.BASE_URL)
        try:
            response = await client.chat.completions.create(
                model=self.MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000,
            )
        except openai.AuthenticationError:
            api_logger.warning("[LlamaProvider] Invalid API key")
            raise ValueError("invalid_key")
        except openai.RateLimitError:
            api_logger.warning("[LlamaProvider] Rate limit / quota exceeded")
            raise ValueError("quota")
        except openai.APITimeoutError:
            api_logger.warning("[LlamaProvider] SDK-level timeout")
            raise ValueError("timeout")
        except openai.APIConnectionError as exc:
            api_logger.error("[LlamaProvider] Connection error: %s", exc)
            raise ValueError("timeout")
        except openai.APIStatusError as exc:
            api_logger.error(
                "[LlamaProvider] API error %d: %s", exc.status_code, exc.message
            )
            raise

        return _parse_json(response.choices[0].message.content, sublevel)


# ---------------------------------------------------------------------------
# Mistral — OpenAI-compatible
# ---------------------------------------------------------------------------

class MistralProvider(AIProvider):
    MODEL = "mistral-small-latest"
    BASE_URL = "https://api.mistral.ai/v1"

    async def _call_once(self, prompt: str, api_key: str, sublevel: str = "") -> dict:
        import openai

        client = openai.AsyncOpenAI(api_key=api_key, base_url=self.BASE_URL)
        try:
            response = await client.chat.completions.create(
                model=self.MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000,
            )
        except openai.AuthenticationError:
            api_logger.warning("[MistralProvider] Invalid API key")
            raise ValueError("invalid_key")
        except openai.RateLimitError:
            api_logger.warning("[MistralProvider] Rate limit / quota exceeded")
            raise ValueError("quota")
        except openai.APITimeoutError:
            api_logger.warning("[MistralProvider] SDK-level timeout")
            raise ValueError("timeout")
        except openai.APIConnectionError as exc:
            api_logger.error("[MistralProvider] Connection error: %s", exc)
            raise ValueError("timeout")
        except openai.APIStatusError as exc:
            api_logger.error(
                "[MistralProvider] API error %d: %s", exc.status_code, exc.message
            )
            raise

        return _parse_json(response.choices[0].message.content, sublevel)


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

_PROVIDERS: dict[str, type[AIProvider]] = {
    "anthropic": ClaudeProvider,
    "openai": OpenAIProvider,
    "gemini": GeminiProvider,
    "grok": GrokProvider,
    "llama": LlamaProvider,
    "mistral": MistralProvider,
}


def get_provider(provider_name: str) -> AIProvider:
    cls = _PROVIDERS.get(provider_name.lower())
    if cls is None:
        raise ValueError(f"Unknown provider: {provider_name!r}")
    return cls()


# ---------------------------------------------------------------------------
# Universal JSON parser
# ---------------------------------------------------------------------------

_REQUIRED_KEYS = {"enonce", "correction", "explication", "deroulement"}


def _parse_json(raw: str, sublevel: str = "") -> dict:
    """Parse AI response to a dict with the 4 exercise fields.

    Strategy:
      1. Strip markdown code fences.
      2. Try direct json.loads.
      3. Fallback: extract the first {...} block with regex.
      4. Fallback: extract content from Markdown sections (## headers).
      5. If all attempts fail, raise ValueError("json").

    Missing fields are logged as a warning but do NOT raise —
    partial data is better than no data.
    """
    # TEMP DIAG — log raw response for intro_poo to diagnose parser failures
    if sublevel == "intro_poo":
        json_logger.warning(
            "[TEMP DIAG intro_poo] Raw AI response:\n--- BEGIN ---\n%s\n--- END ---",
            raw,
        )

    cleaned = re.sub(r"```(?:json)?\s*", "", raw).replace("```", "").strip()

    data: dict | None = None

    # Attempt 1 — direct parse
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        json_logger.warning("JSON direct parse failed: %s", exc)

    # Attempt 2 — extract first {...} block
    if data is None:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group())
            except json.JSONDecodeError as exc:
                json_logger.warning("JSON block extraction failed: %s", exc)

    # Attempt 3 — extract content from Markdown ## sections
    if data is None:
        data = _parse_markdown_sections(raw)
        if data is not None:
            json_logger.warning("JSON parsing failed — recovered via Markdown section extraction")

    if data is None:
        json_logger.error(
            "JSON parsing failed completely.\n--- RAW RESPONSE ---\n%s\n--- END RAW RESPONSE ---",
            raw,
        )
        raise ValueError("json")

    # QCM format returns a JSON array — wrap it for uniform return type
    if isinstance(data, list):
        return {"_qcm_list": data}

    missing = _REQUIRED_KEYS - data.keys()
    if missing:
        json_logger.warning("AI response missing keys: %s", missing)

    return data


def _parse_markdown_sections(raw: str) -> dict | None:
    """Fallback: extract exercise fields from a Markdown-formatted response.

    Recognises headers of the form:
        ## Énoncé  /  ## 1)  /  ## 1. Énoncé  …
        ## Correction  /  ## 2)  …
        ## Explication  /  ## 3)  …
        ## Déroulement  /  ## 4)  …

    Returns a dict with the 4 keys, or None if no matching header is found.
    """

    def _map_header(text: str) -> str | None:
        t = text.strip()
        tl = t.lower()
        if re.search(r"[eé]nonc[eé]", tl) or re.match(r"^1[\s.):-]|^1$", t):
            return "enonce"
        if re.search(r"correction", tl) or re.match(r"^2[\s.):-]|^2$", t):
            return "correction"
        if re.search(r"explication", tl) or re.match(r"^3[\s.):-]|^3$", t):
            return "explication"
        if re.search(r"d[eé]roulement", tl) or re.match(r"^4[\s.):-]|^4$", t):
            return "deroulement"
        return None

    header_re = re.compile(r"^##\s+(.+)$", re.MULTILINE)
    headers = list(header_re.finditer(raw))

    if not headers:
        return None

    result: dict[str, str] = {k: "" for k in ("enonce", "correction", "explication", "deroulement")}
    found_any = False

    for i, match in enumerate(headers):
        key = _map_header(match.group(1))
        if key is None:
            continue
        found_any = True
        content_start = match.end()
        content_end = headers[i + 1].start() if i + 1 < len(headers) else len(raw)
        result[key] = raw[content_start:content_end].strip()

    return result if found_any else None
