import json
import os
import sys


def _is_android() -> bool:
    return (
        os.path.exists("/data/user/0")
        or "ANDROID_ROOT" in os.environ
        or "ANDROID_DATA" in os.environ
    )


def _get_settings_path() -> str:
    if _is_android():
        # Flet/Android expose le répertoire de données via cette variable d'env
        # Ce chemin n'est disponible qu'une fois Flet initialisé — ne pas appeler
        # cette fonction au niveau module, uniquement depuis __init__
        data_dir = os.environ.get("FLET_APP_DATA_DIR", "")
        if not data_dir:
            # Fallback robuste : /data/data/<package>/files (toujours accessible)
            import glob as _glob
            candidates = _glob.glob("/data/data/*/files")
            if candidates:
                data_dir = candidates[0]
            else:
                data_dir = "/data/data/forpy/files"
        return os.path.join(data_dir, "settings.json")
    # Windows (win32) et Linux : ~/.forpy/
    settings_dir = os.path.expanduser("~/.forpy")
    os.makedirs(settings_dir, exist_ok=True)
    return os.path.join(settings_dir, "settings.json")

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
        self.current_pattern_category: str = ""
        self.current_pattern: str = ""
        self.current_logic_image: str = ""

        # Chemin calculé ici (après init Flet) et non au niveau module
        self._settings_path: str = _get_settings_path()

        # Persistent settings
        self._settings: dict = self._load_settings()

    # ------------------------------------------------------------------
    # Settings persistence
    # ------------------------------------------------------------------

    def _load_settings(self) -> dict:
        if os.path.exists(self._settings_path):
            try:
                with open(self._settings_path, encoding="utf-8") as f:
                    data = json.load(f)
                return {**DEFAULT_SETTINGS, **data}
            except (json.JSONDecodeError, OSError):
                pass
        return dict(DEFAULT_SETTINGS)

    def save_settings(self) -> None:
        with open(self._settings_path, "w", encoding="utf-8") as f:
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
        """Select a new sublevel and reset the anti-repetition topic and pattern."""
        if self.current_sublevel != sublevel:
            self.last_exercise_topic = ""
            self.current_pattern_category = ""
            self.current_pattern = ""
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
