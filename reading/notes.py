"""My reading notes: reading status, summary notes in my own words and practice questions, per account.

Saved in book_notes.json next to the project files (git-ignored, never uploaded): the notes are for
personal study, and only short quotes from the books are allowed (QUOTE_LIMIT) so they stay my own work.
"""

import json
import random
import uuid
from datetime import datetime
from pathlib import Path

NOTES_FILE = Path(__file__).resolve().parent.parent / "book_notes.json"
QUOTE_LIMIT = 300  # characters: a short quote, the rest goes in my own words
STATUSES = ("to_read", "reading", "done")


def _load_all() -> dict:
    try:
        return json.loads(NOTES_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _save_all(data: dict) -> None:
    NOTES_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def load(user: str) -> dict:
    """{"status": {book_id: status}, "notes": [note, ...]} for one account."""
    mine = _load_all().get(user, {})
    return {"status": mine.get("status", {}), "notes": mine.get("notes", [])}


def _save(user: str, mine: dict) -> None:
    data = _load_all()
    data[user] = mine
    _save_all(data)


def set_status(user: str, book_id: str, status: str) -> None:
    if status not in STATUSES:
        raise ValueError(status)
    mine = load(user)
    mine["status"][book_id] = status
    _save(user, mine)


def clean_cards(cards: list[dict]) -> list[dict]:
    return [{"q": c["q"].strip(), "a": c["a"].strip()} for c in cards if c.get("q", "").strip() and c.get("a", "").strip()]


def check(summary: str, quote: str) -> list[str]:
    """Problems with a note before saving (empty = fine). Returned as English keys for t()."""
    problems = []
    if not summary.strip():
        problems.append("Write the summary in your own words.")
    if len(quote) > QUOTE_LIMIT:
        problems.append("The quote is too long – keep it short and put the rest in your own words.")
    return problems


def save_note(user: str, book_id: str, page: str, summary: str, quote: str, cards: list[dict],
              note_id: str | None = None) -> str:
    """Add a note (or replace the one with note_id). Returns its id."""
    if check(summary, quote):
        raise ValueError(check(summary, quote))
    mine = load(user)
    now = datetime.now().isoformat(timespec="seconds")
    note = {"id": note_id or uuid.uuid4().hex[:8], "book": book_id, "page": page.strip(), "summary": summary.strip(),
            "quote": quote.strip(), "cards": clean_cards(cards), "updated": now}
    old = next((n for n in mine["notes"] if n["id"] == note["id"]), None)
    note["created"] = old["created"] if old else now
    mine["notes"] = [n for n in mine["notes"] if n["id"] != note["id"]] + [note]
    if mine["status"].get(book_id, "to_read") == "to_read":
        mine["status"][book_id] = "reading"  # writing notes means I've started it
    _save(user, mine)
    return note["id"]


def delete_note(user: str, note_id: str) -> None:
    mine = load(user)
    mine["notes"] = [n for n in mine["notes"] if n["id"] != note_id]
    _save(user, mine)


def notes_for(mine: dict, book_id: str) -> list[dict]:
    return sorted((n for n in mine["notes"] if n["book"] == book_id), key=lambda n: n["created"])


def cards(mine: dict, book_ids: set[str] | None = None) -> list[dict]:
    """All practice questions, each with the book and page it came from."""
    return [{**c, "book": n["book"], "page": n["page"]} for n in mine["notes"]
            if book_ids is None or n["book"] in book_ids for c in n["cards"]]


def draw(deck: list[dict], avoid: dict | None = None) -> dict | None:
    """A random card, not the same one twice in a row when there is a choice."""
    choices = [c for c in deck if c != avoid] or deck
    return random.choice(choices) if choices else None
