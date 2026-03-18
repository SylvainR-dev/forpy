"""
Tests for services/ai_service.py

Covers:
- _parse_json  : all parsing paths (direct, markdown, embedded, invalid, missing keys)
- get_provider : factory for known and unknown names
- call_async   : retry on timeout, retry on json error, no retry on invalid_key / quota,
                 max retries exhausted, success on second attempt
"""
import asyncio
import pytest
from unittest.mock import AsyncMock, patch

from services.ai_service import _parse_json, get_provider, ClaudeProvider, MAX_RETRIES


# ──────────────────────────────────────────────────────────────────────────────
# _parse_json
# ──────────────────────────────────────────────────────────────────────────────

class TestParseJson:
    VALID = '{"enonce":"Q","correction":"A","explication":"E","deroulement":"D"}'
    VALID_DICT = {"enonce": "Q", "correction": "A", "explication": "E", "deroulement": "D"}

    def test_direct_json(self):
        assert _parse_json(self.VALID) == self.VALID_DICT

    def test_markdown_backticks_stripped(self):
        raw = f"```json\n{self.VALID}\n```"
        assert _parse_json(raw) == self.VALID_DICT

    def test_markdown_no_lang_stripped(self):
        raw = f"```\n{self.VALID}\n```"
        assert _parse_json(raw) == self.VALID_DICT

    def test_json_embedded_in_text(self):
        raw = f"Here is your exercise:\n{self.VALID}\nEnjoy!"
        assert _parse_json(raw) == self.VALID_DICT

    def test_invalid_json_raises_value_error(self):
        with pytest.raises(ValueError) as exc_info:
            _parse_json("not json at all !!!")
        assert str(exc_info.value) == "json"

    def test_completely_empty_raises_value_error(self):
        with pytest.raises(ValueError) as exc_info:
            _parse_json("")
        assert str(exc_info.value) == "json"

    def test_missing_keys_does_not_raise(self):
        """Partial data is better than no data — missing keys only warn."""
        raw = '{"enonce": "Q", "correction": "A"}'
        result = _parse_json(raw)
        assert result["enonce"] == "Q"
        assert result["correction"] == "A"

    def test_extra_keys_preserved(self):
        raw = '{"enonce":"Q","correction":"A","explication":"E","deroulement":"D","extra":"X"}'
        result = _parse_json(raw)
        assert result["extra"] == "X"

    def test_unicode_content(self):
        raw = '{"enonce":"Créez une liste","correction":"lst = []","explication":"Ligne 1","deroulement":"Flux"}'
        result = _parse_json(raw)
        assert result["enonce"] == "Créez une liste"


# ──────────────────────────────────────────────────────────────────────────────
# get_provider
# ──────────────────────────────────────────────────────────────────────────────

class TestGetProvider:
    def test_anthropic_returns_claude_provider(self):
        from services.ai_service import ClaudeProvider
        assert isinstance(get_provider("anthropic"), ClaudeProvider)

    def test_openai_returns_openai_provider(self):
        from services.ai_service import OpenAIProvider
        assert isinstance(get_provider("openai"), OpenAIProvider)

    def test_gemini_returns_gemini_provider(self):
        from services.ai_service import GeminiProvider
        assert isinstance(get_provider("gemini"), GeminiProvider)

    def test_case_insensitive(self):
        from services.ai_service import ClaudeProvider
        assert isinstance(get_provider("Anthropic"), ClaudeProvider)
        assert isinstance(get_provider("OPENAI"), get_provider("openai").__class__)

    def test_unknown_provider_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown provider"):
            get_provider("grok")


# ──────────────────────────────────────────────────────────────────────────────
# call_async  — retry logic  (no real API calls, _call_once is mocked)
# ──────────────────────────────────────────────────────────────────────────────

GOOD_RESPONSE = {
    "enonce": "Q", "correction": "A",
    "explication": "E", "deroulement": "D",
}


class TestCallAsyncRetry:
    """
    Retry rules from architecture:
        timeout  → retry up to MAX_RETRIES times
        json     → retry up to MAX_RETRIES times
        invalid_key / quota → raise immediately (no retry)
    """

    async def test_success_on_first_attempt(self):
        provider = ClaudeProvider()
        mock = AsyncMock(return_value=GOOD_RESPONSE)
        with patch.object(provider, "_call_once", mock):
            result = await provider.call_async("prompt", "key")
        assert result == GOOD_RESPONSE
        assert mock.call_count == 1

    async def test_timeout_is_retried_and_succeeds(self):
        provider = ClaudeProvider()
        call_count = 0

        async def flaky(prompt, api_key):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("timeout")
            return GOOD_RESPONSE

        with patch.object(provider, "_call_once", flaky):
            result = await provider.call_async("prompt", "key")

        assert result == GOOD_RESPONSE
        assert call_count == 2

    async def test_json_error_is_retried_and_succeeds(self):
        provider = ClaudeProvider()
        call_count = 0

        async def flaky(prompt, api_key):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("json")
            return GOOD_RESPONSE

        with patch.object(provider, "_call_once", flaky):
            result = await provider.call_async("prompt", "key")

        assert result == GOOD_RESPONSE
        assert call_count == 2

    async def test_timeout_exhausts_max_retries_and_raises(self):
        provider = ClaudeProvider()
        mock = AsyncMock(side_effect=ValueError("timeout"))

        with patch.object(provider, "_call_once", mock):
            with pytest.raises(ValueError) as exc_info:
                await provider.call_async("prompt", "key")

        assert str(exc_info.value) == "timeout"
        assert mock.call_count == MAX_RETRIES

    async def test_json_exhausts_max_retries_and_raises(self):
        provider = ClaudeProvider()
        mock = AsyncMock(side_effect=ValueError("json"))

        with patch.object(provider, "_call_once", mock):
            with pytest.raises(ValueError) as exc_info:
                await provider.call_async("prompt", "key")

        assert str(exc_info.value) == "json"
        assert mock.call_count == MAX_RETRIES

    async def test_invalid_key_not_retried(self):
        provider = ClaudeProvider()
        mock = AsyncMock(side_effect=ValueError("invalid_key"))

        with patch.object(provider, "_call_once", mock):
            with pytest.raises(ValueError) as exc_info:
                await provider.call_async("prompt", "key")

        assert str(exc_info.value) == "invalid_key"
        assert mock.call_count == 1  # no retry

    async def test_quota_not_retried(self):
        provider = ClaudeProvider()
        mock = AsyncMock(side_effect=ValueError("quota"))

        with patch.object(provider, "_call_once", mock):
            with pytest.raises(ValueError) as exc_info:
                await provider.call_async("prompt", "key")

        assert str(exc_info.value) == "quota"
        assert mock.call_count == 1  # no retry

    async def test_asyncio_timeout_is_retried(self):
        """asyncio.wait_for timeout is also retried."""
        provider = ClaudeProvider()
        call_count = 0

        async def slow(prompt, api_key):
            nonlocal call_count
            call_count += 1
            if call_count < MAX_RETRIES:
                raise asyncio.TimeoutError()
            return GOOD_RESPONSE

        with patch.object(provider, "_call_once", slow):
            result = await provider.call_async("prompt", "key")

        assert result == GOOD_RESPONSE
        assert call_count == MAX_RETRIES
