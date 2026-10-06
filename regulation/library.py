"""All Law & Regulation entries in one list, with search, filters and a self-check.

Run `python -m regulation.library` to check every entry has its texts, a source with a link and
valid dates.
"""

from datetime import date

from regulation import topic_a, topic_b, topic_c, topic_d, topic_e
from regulation.model import ROLES, TOPICS, Entry, Table

_TOPICS = (topic_a, topic_b, topic_c, topic_d, topic_e)
ENTRIES: list[Entry] = [e for t in _TOPICS for e in t.ENTRIES]
TABLES: list[Table] = [tb for t in _TOPICS for tb in getattr(t, "TABLES", [])]


def topics_with_entries() -> list[str]:
    return [k for k in TOPICS if any(e.topic == k for e in ENTRIES)]


def modules_with_entries() -> list[int]:
    return sorted({m for e in ENTRIES for m in e.modules})


def _haystack(entry: Entry) -> str:
    texts = [entry.id, *entry.keywords, *entry.title.values(), *entry.summary.values()]
    texts += [t for p in entry.points for t in p.values()]
    texts += [s.code for s in entry.sources] + [t for s in entry.sources for t in s.title.values()]
    return " ".join(texts).lower()


def find(query: str = "", topic: str | None = None, module: int | None = None,
         role: str | None = None) -> list[Entry]:
    """Entries matching all the given filters. `query` matches English or Thai text, codes and keywords;
    every word of it must appear."""
    words = query.lower().split()
    return [e for e in ENTRIES
            if (topic is None or e.topic == topic)
            and (module is None or module in e.modules)
            and (role is None or role in e.roles)
            and all(w in _haystack(e) for w in words)]


def problems() -> list[str]:
    """Things to fix in the entries (empty list = all good)."""
    found, seen = [], set()
    for e in ENTRIES:
        where = f"{e.id}:"
        if e.id in seen:
            found.append(f"{where} duplicate id")
        seen.add(e.id)
        if e.topic not in TOPICS:
            found.append(f"{where} unknown topic {e.topic}")
        for text in (e.title, e.summary, *e.points, *(s.title for s in e.sources)):
            if not (text.get("en") and text.get("th")):
                found.append(f"{where} text missing English or Thai: {text}")
        if not e.sources:
            found.append(f"{where} no source")
        for s in e.sources:
            if not s.url.startswith("https://"):
                found.append(f"{where} source {s.code} has no https link")
        for value, name in ((e.checked, "checked"), (e.effective, "effective")):
            if value or name == "checked":
                try:
                    if date.fromisoformat(value) > date.today():
                        found.append(f"{where} {name} date is in the future")
                except ValueError:
                    found.append(f"{where} {name} is not a YYYY-MM-DD date: {value!r}")
        found += [f"{where} unknown role {r}" for r in e.roles if r not in ROLES]
        found += [f"{where} module {m} is not 1-6" for m in e.modules if m not in range(1, 7)]
        if not e.modules:
            found.append(f"{where} no CFP module")
    for tb in TABLES:
        where = f"table {tb.title.get('en')}:"
        if tb.topic not in TOPICS:
            found.append(f"{where} unknown topic {tb.topic}")
        for row in tb.rows:
            if len(row) != len(tb.header):
                found.append(f"{where} row has {len(row)} cells, header has {len(tb.header)}")
        for text in (tb.title, *tb.header, *(c for r in tb.rows for c in r if isinstance(c, dict))):
            if not (text.get("en") and text.get("th")):
                found.append(f"{where} text missing English or Thai: {text}")
    return found


if __name__ == "__main__":
    issues = problems()
    print(f"{len(ENTRIES)} entries, {len(issues)} problems")
    print("\n".join(issues))
