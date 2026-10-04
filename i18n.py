"""English / Thai text for the whole app.

Write every on-screen text in English through t():   st.title(t("Financial calculator"))
Text with values uses {placeholders}:                 t("Data starts {date}", date=...)
Thai translations live in i18n_th.py (English text -> Thai). Text without a Thai entry stays
English, so nothing breaks while a translation is missing; check_translations() lists them.

The chosen language is saved in user_settings.json next to this file, so it survives a browser
refresh and an app restart. (This app runs on one computer for one person, so a file is the
simplest place to remember it.)
"""

import json
from pathlib import Path

import streamlit as st

from i18n_th import TH

SETTINGS_FILE = Path(__file__).parent / "user_settings.json"
LANGUAGES = {"en": "English", "th": "ไทย"}


def _load_settings() -> dict:
    try:
        return json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _save_settings(settings: dict) -> None:
    try:
        SETTINGS_FILE.write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        pass  # can't save: the choice still works until the browser tab is closed


def lang() -> str:
    """Current language code: 'en' or 'th'."""
    if "lang" not in st.session_state:
        saved = _load_settings().get("lang")
        st.session_state["lang"] = saved if saved in LANGUAGES else "en"
    return st.session_state["lang"]


def t(text: str, **values) -> str:
    """Text in the current language, with {placeholders} filled from `values`."""
    if lang() == "th":
        text = TH.get(text, text)
    return text.format(**values) if values else text


def language_switcher() -> None:
    """English | ไทย switch. Remembers the choice in user_settings.json."""
    def changed():
        st.session_state["lang"] = st.session_state["lang_switch"]
        _save_settings({**_load_settings(), "lang": st.session_state["lang"]})

    st.radio("Language / ภาษา", list(LANGUAGES), format_func=LANGUAGES.get,
             index=list(LANGUAGES).index(lang()), key="lang_switch", horizontal=True,
             on_change=changed, label_visibility="collapsed")


def check_translations(paths: list[str]) -> list[str]:
    """English texts passed to t() in these files that have no Thai translation yet."""
    import ast

    missing = []
    for path in paths:
        tree = ast.parse(Path(path).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call) and getattr(node.func, "id", None) == "t" and node.args
                    and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str)
                    and node.args[0].value not in TH):
                missing.append(f"{path}:{node.lineno}: {node.args[0].value}")
    return missing
