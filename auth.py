"""Log in, roles, and which part of the app each account can see.

Accounts are saved in users.json next to this file. It is git-ignored, so it is never uploaded
to GitHub. Passwords are never stored: only a salted PBKDF2 hash of each one.

Roles:
  superadmin  sees every page and manages accounts on the Admin page
  user        sees only the areas a superadmin gave them (Tools, Reference, Career, Module 1-6)

Pages a person may not see are not given to st.navigation at all, so they cannot be opened by
typing their URL either.
"""

import hashlib
import hmac
import json
import re
import secrets
import time
from datetime import datetime

import streamlit as st

from cfp_modules import MODULES
from edition import USER_DIR
from i18n import lang, t
from user_settings import load_settings, save_setting

USERS_FILE = USER_DIR / "users.json"

# Login on/off. While False the app opens straight in, everyone is treated as the superadmin
# "local", and the login, account and admin pages are hidden. Set to True to require log in.
LOGIN_ENABLED = False
LOCAL_USER = {"username": "local", "name": "local", "role": "superadmin", "areas": [], "disabled": False}

ROLES = ["superadmin", "user"]
AREAS = ["tools", "reference", "career"] + [f"m{m.number}" for m in MODULES]

ITERATIONS = 200_000      # PBKDF2 rounds: slow on purpose, so guessing passwords is slow too
MIN_PASSWORD = 8
MAX_FAILS = 5             # wrong passwords in a row before the account is locked ...
LOCK_SECONDS = 5 * 60     # ... for this long
IDLE_MINUTES = 60         # log out after this long without using the app
USERNAME_RE = re.compile(r"^[a-z0-9_.-]{3,30}$")


# ---------- accounts file ----------

def load_users() -> dict:
    """{username: {name, role, areas, salt, hash, disabled, created}}"""
    try:
        return json.loads(USERS_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_users(users: dict) -> None:
    USERS_FILE.write_text(json.dumps(users, ensure_ascii=False, indent=2), encoding="utf-8")


def _hash(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), ITERATIONS).hex()


def set_password(record: dict, password: str) -> None:
    record["salt"] = secrets.token_hex(16)
    record["hash"] = _hash(password, record["salt"])


def password_ok(record: dict, password: str) -> bool:
    return hmac.compare_digest(_hash(password, record["salt"]), record["hash"])


def new_account(name: str, role: str, areas: list[str], password: str) -> dict:
    record = {"name": name, "role": role, "areas": areas, "disabled": False,
              "created": datetime.now().strftime("%Y-%m-%d %H:%M")}
    set_password(record, password)
    return record


def check_username(username: str, users: dict) -> str | None:
    """Error message for a new username, or None if it is fine."""
    if not USERNAME_RE.match(username):
        return t("Username: 3-30 characters, only a-z, 0-9, dot, dash or underscore.")
    if username in users:
        return t("This username already exists.")
    return None


def check_new_password(password: str, confirm: str) -> str | None:
    if len(password) < MIN_PASSWORD:
        return t("Password needs at least {n} characters.", n=MIN_PASSWORD)
    if password != confirm:
        return t("The two passwords are not the same.")
    return None


def active_superadmins(users: dict) -> list[str]:
    return [u for u, r in users.items() if r["role"] == "superadmin" and not r.get("disabled")]


def area_label(area: str) -> str:
    if area == "tools":
        return t("Tools (financial calculator)")
    if area == "career":
        return t("CFP career guide")
    if area == "reference":
        return t("Law & Regulation")
    m = MODULES[int(area[1:]) - 1]
    return t("Module {n}", n=m.number) + " · " + (m.name_th if lang() == "th" else m.name_en)


# ---------- who is logged in ----------

def current_user() -> dict | None:
    """The logged-in account (with 'username' added), or None.

    Read from users.json on every page run, so a change by the superadmin (disable, fewer areas)
    takes effect on that person's next click.
    """
    if not LOGIN_ENABLED:
        return dict(LOCAL_USER)
    username = st.session_state.get("auth_user")
    if not username:
        return None
    record = load_users().get(username)
    if record is None or record.get("disabled"):
        logout()
        return None
    if time.time() - st.session_state.get("auth_last_active", 0) > IDLE_MINUTES * 60:
        logout(t("You were logged out after {n} minutes without activity.", n=IDLE_MINUTES))
        return None
    st.session_state["auth_last_active"] = time.time()
    return {"username": username, **record}


def is_superadmin(user: dict | None) -> bool:
    return bool(user) and user["role"] == "superadmin"


def can(user: dict | None, area: str) -> bool:
    """May this account see this area ('tools', 'career', 'm1' ... 'm6')?"""
    return is_superadmin(user) or (bool(user) and area in user.get("areas", []))


def logout(message: str | None = None) -> None:
    for key in ("auth_user", "auth_last_active"):
        st.session_state.pop(key, None)
    if message:
        st.session_state["auth_message"] = message


def _start_session(username: str) -> None:
    st.session_state["auth_user"] = username
    st.session_state["auth_last_active"] = time.time()


@st.cache_resource
def _failed_logins() -> dict:
    """{username: (fails in a row, locked until)}, shared by all browser tabs on this server."""
    return {}


# ---------- log in / first-time setup (the screens are in interface/login.py) ----------

def create_first_superadmin(username: str, name: str, password: str) -> None:
    """Save the first account as superadmin and log it in."""
    save_users({username: new_account(name.strip() or username, "superadmin", AREAS, password)})
    # CFP progress saved before accounts existed belongs to this first account.
    old = load_settings().get("cfp_progress") or {}
    if "trained" in old:
        save_setting("cfp_progress", {username: old})
    elif LOCAL_USER["username"] in old:
        old[username] = old.pop(LOCAL_USER["username"])
        save_setting("cfp_progress", old)
    _start_session(username)


def try_login(username: str, password: str) -> tuple[str, int]:
    """Check a log in. Returns ("ok", 0), ("locked", minutes left) or ("wrong", 0)."""
    failed = _failed_logins()
    fails, locked_until = failed.get(username, (0, 0))
    if time.time() < locked_until:
        return "locked", int((locked_until - time.time()) // 60) + 1

    record = load_users().get(username)
    if record and not record.get("disabled") and password_ok(record, password):
        failed.pop(username, None)
        _start_session(username)
        return "ok", 0

    fails += 1
    failed[username] = (fails, time.time() + LOCK_SECONDS if fails >= MAX_FAILS else 0)
    time.sleep(1)  # slows down guessing
    return "wrong", 0
