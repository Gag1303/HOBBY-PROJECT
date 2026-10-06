"""Watch the SEC's rules database for new documents that may change the Law & Regulation entries.

The SEC lists every new rule, guideline and circular in its yearly index ("กฎหมายและประกาศที่ออกรายปี"
in the NRS law search). check() reads that index for this year (and last year too in January), keeps
what it found in data/sec_watch.json (git-ignored) and remembers which documents were already reviewed.

A document is linked to an entry when its title contains one of the `watch` words of a source the
entry is based on (see regulation/sources.py). The watcher never changes an entry: a flagged entry
needs a person to read the new document and update the summary.

Run `python -m regulation.watcher` to check now and print what was found.
"""

import html
import json
import re
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path

from regulation.library import ENTRIES
from regulation.model import Entry

INDEX_URL = "https://capital.sec.or.th/webapp/nrs/nrs_table_of_contents.php"
STATE_FILE = Path(__file__).resolve().parent.parent / "data" / "sec_watch.json"
# the SEC site blocks unknown programs, so ask like a normal browser
USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/130.0 Safari/537.36 Edg/130.0")
# title words that make a document worth seeing even when it matches no source yet
TOPIC_WORDS = ("กองทุนรวม", "หน่วยลงทุน", "บุคลากร", "ผู้แนะนำการลงทุน", "ผู้วางแผนการลงทุน",
               "นักวิเคราะห์การลงทุน", "ผู้จัดการกองทุน", "ผู้ดูแลผลประโยชน์", "ผู้ลงทุน", "ลูกค้า")


@dataclass(frozen=True)
class Notice:
    id: str        # the SEC's file number (e.g. "11092"), or number + date when there is no file
    number: str    # e.g. "นจ.(ว) 2/2569"
    issued: str    # ISO date
    title: str
    url: str       # readable PDF ("" if none)
    active: bool   # False when the SEC marks it cancelled
    baseline: bool = False  # already listed the first time the watcher ran

    def related(self) -> list[Entry]:
        """Entries based on a source this document seems to change."""
        return [e for e in ENTRIES if any(w in self.title for s in e.sources for w in s.watch)]

    def relevant(self) -> bool:
        return bool(self.related()) or any(w in self.title for w in TOPIC_WORDS)

    def affects(self, entry: Entry) -> bool:
        """Newer than the last time the entry was checked (or first seen after the watcher started)."""
        return self.issued >= entry.checked or not self.baseline


# ---------- reading the SEC index ----------

def _be_date(text: str) -> str:
    day, month, year_be = (int(x) for x in text.split("/"))
    return date(year_be - 543, month, day).isoformat()


def parse_index(page: str) -> list[Notice]:
    """Notices in one yearly index page (HTML already decoded)."""
    notices = []
    for row in re.findall(r"<tr bgcolor=#(?:D9E9F5|F4E1C6)>(.*?)</tr>", page, re.S):
        cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)]
        if len(cells) < 3 or not re.fullmatch(r"\d\d/\d\d/\d{4}", cells[1]):
            continue
        number, issued, title = cells[0], _be_date(cells[1]), re.sub(r"\s+", " ", cells[2])
        if "/" not in number:
            number = f"{number}/{cells[1][-4:]}"
        pdf = re.search(r"(https://publish\.sec\.or\.th/nrs/(\d+)p_r\.pdf)", row)
        any_file = re.search(r"https://publish\.sec\.or\.th/nrs/(\d+)\w*\.\w+", row)
        notices.append(Notice(
            id=any_file.group(1) if any_file else f"{number} {issued}",
            number=number, issued=issued, title=title,
            url=pdf.group(1) if pdf else (any_file.group(0) if any_file else ""),
            active="title='ยกเลิก'" not in row))
    return notices


def fetch_year(year: int) -> list[Notice]:
    """All documents the SEC issued in a calendar year (raises if the site can't be read)."""
    form = urllib.parse.urlencode({"text_year": str(year + 543), "doc_type[]": "0"}).encode()
    request = urllib.request.Request(INDEX_URL, data=form, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        page = response.read().decode("tis-620", errors="replace")
    notices = parse_index(page)
    if not notices and "nrs" not in page:
        raise RuntimeError("the SEC page did not look like the rules index")
    return notices


# ---------- saved state ----------

def load_state() -> dict:
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"last_check": None, "last_try": None, "error": None, "notices": [], "reviewed": []}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")


def notices(state: dict) -> list[Notice]:
    return [Notice(**n) for n in state["notices"]]


def is_due(state: dict, today: date | None = None) -> bool:
    """True when no check was tried today (so the app checks at most once a day by itself)."""
    today = today or date.today()
    return not state.get("last_try") or state["last_try"][:10] < today.isoformat()


def check(today: date | None = None) -> dict:
    """Read the SEC index, merge it into the saved state and save. Errors are kept in state["error"]."""
    today = today or date.today()
    state = load_state()
    now = datetime.now().isoformat(timespec="seconds")
    state["last_try"] = now
    years = [today.year - 1, today.year] if today.month == 1 else [today.year]
    try:
        found = [n for y in years for n in fetch_year(y)]
    except Exception as error:  # no internet, site blocked or changed: keep what we had
        state["error"] = f"{type(error).__name__}: {error}"
        save_state(state)
        return state
    first_run = not state["notices"]
    known = {n["id"]: n for n in state["notices"]}
    merged = []
    for n in found:
        old = known.get(n.id)
        baseline = first_run or bool(old and old.get("baseline"))
        merged.append(asdict(Notice(**{**asdict(n), "baseline": baseline})))
    # keep older years we already had, so nothing disappears in January
    found_ids = {n["id"] for n in merged}
    merged += [n for n in state["notices"] if n["id"] not in found_ids and n["issued"][:4] >= str(today.year - 1)]
    state.update(last_check=now, error=None, notices=sorted(merged, key=lambda n: n["issued"], reverse=True))
    save_state(state)
    return state


def mark_reviewed(ids: list[str]) -> None:
    state = load_state()
    state["reviewed"] = sorted(set(state["reviewed"]) | set(ids))
    save_state(state)


# ---------- what to show ----------

def relevant(state: dict) -> list[Notice]:
    """Documents this year that touch our topics, newest first."""
    return [n for n in notices(state) if n.relevant()]


def unreviewed(state: dict) -> list[Notice]:
    """Relevant documents that may change an entry and have not been marked as reviewed."""
    reviewed = set(state["reviewed"])
    oldest_check = min(e.checked for e in ENTRIES)
    return [n for n in relevant(state) if n.id not in reviewed
            and (any(n.affects(e) for e in n.related()) or (not n.related() and n.issued >= oldest_check))]


def flags(state: dict) -> dict[str, list[Notice]]:
    """Entry id -> unreviewed documents that may change it."""
    found: dict[str, list[Notice]] = {}
    for n in unreviewed(state):
        for e in n.related():
            if n.affects(e):
                found.setdefault(e.id, []).append(n)
    return found


if __name__ == "__main__":
    s = check()
    print("error:", s["error"]) if s["error"] else None
    print(f"{len(s['notices'])} SEC documents this year, {len(relevant(s))} relevant, "
          f"{len(unreviewed(s))} not reviewed")
    for n in unreviewed(s):
        print(" -", n.number, n.issued, n.title[:80], [e.id for e in n.related() if n.affects(e)])
