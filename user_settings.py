"""Personal settings saved on this computer (language, CFP progress, ...).

Stored in user_settings.json next to this file, which is git-ignored, so it survives a browser
refresh and an app restart but is never uploaded to GitHub.
"""

import json
from pathlib import Path

SETTINGS_FILE = Path(__file__).parent / "user_settings.json"


def load_settings() -> dict:
    try:
        return json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_setting(key: str, value) -> None:
    """Save one setting, keeping the others."""
    settings = load_settings()
    settings[key] = value
    try:
        SETTINGS_FILE.write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        pass  # can't save: the value still works until the browser tab is closed
