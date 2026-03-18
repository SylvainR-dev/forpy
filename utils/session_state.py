import json
import os

SETTINGS_PATH = "settings.json"

DEFAULT_SETTINGS = {
    "api_key": "",
    "provider": "anthropic",
    "interface_language": "english",
    "exercise_language": "english",
    "theme": "dark",
}


class SessionState:
    """
    Manages runtime state and persistent user settings.

    Runtime state (in-memory only):
        current_chapter     — e.g. "python"
        current_level       — e.g. "Débutant"
        current_sublevel    — e.g. "debutant_plus"
        last_exercise_topic — last generated topic (anti-repetition)

    Persistent settings (read/written to settings.json):
        api_key, provider, interface_language, exercise_language
    """

    def __init__(self):
        # Runtime navigation state
        self.current_chapter: str = "python"
        self.current_level: str = ""
        self.current_sublevel: str = ""
        self.last_exercise_topic: str = ""

        # Persistent settings
        self._settings: dict = self._load_settings()

    # ------------------------------------------------------------------
    # Settings persistence
    # ------------------------------------------------------------------

    def _load_settings(self) -> dict:
        if os.path.exists(SETTINGS_PATH):
            try:
                with open(SETTINGS_PATH, encoding="utf-8") as f:
                    data = json.load(f)
                return {**DEFAULT_SETTINGS, **data}
            except (json.JSONDecodeError, OSError):
                pass
        return dict(DEFAULT_SETTINGS)

    def save_settings(self) -> None:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(self._settings, f, indent=4, ensure_ascii=False)

    # ------------------------------------------------------------------
    # Settings accessors
    # ------------------------------------------------------------------

    @property
    def api_key(self) -> str:
        return self._settings.get("api_key", "")

    @api_key.setter
    def api_key(self, value: str) -> None:
        self._settings["api_key"] = value

    @property
    def provider(self) -> str:
        return self._settings.get("provider", "anthropic")

    @provider.setter
    def provider(self, value: str) -> None:
        self._settings["provider"] = value

    @property
    def interface_language(self) -> str:
        return self._settings.get("interface_language", "english")

    @interface_language.setter
    def interface_language(self, value: str) -> None:
        self._settings["interface_language"] = value

    @property
    def exercise_language(self) -> str:
        return self._settings.get("exercise_language", "english")

    @exercise_language.setter
    def exercise_language(self, value: str) -> None:
        self._settings["exercise_language"] = value

    # ------------------------------------------------------------------
    # Navigation helpers
    # ------------------------------------------------------------------

    def set_sublevel(self, level: str, sublevel: str) -> None:
        """Select a new sublevel and reset the anti-repetition topic."""
        if self.current_sublevel != sublevel:
            self.last_exercise_topic = ""
        self.current_level = level
        self.current_sublevel = sublevel

    def update_last_topic(self, topic: str) -> None:
        self.last_exercise_topic = topic

    @property
    def theme(self) -> str:
        return self._settings.get("theme", "dark")

    @theme.setter
    def theme(self, value: str) -> None:
        self._settings["theme"] = value
