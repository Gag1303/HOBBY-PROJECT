"""Building blocks of the Law & Regulation reference.

Every rule is one Entry: a short summary in English and Thai, the official source(s) it comes from,
when that version took effect, and when I last checked it against the source. Entries are a personal
study summary, not legal advice: the linked official document is what counts.
"""

from dataclasses import dataclass, field
from datetime import date

# Each text is {"en": ..., "th": ...}; the page shows the one for the current language.
Text = dict

TOPICS = {
    "A": {"en": "Licences & career path", "th": "ใบอนุญาตและเส้นทางอาชีพ"},
    "B": {"en": "Conduct with clients", "th": "การปฏิบัติต่อลูกค้า"},
    "C": {"en": "Penalties", "th": "บทลงโทษ"},
    "D": {"en": "Fund structure", "th": "โครงสร้างกองทุนรวม"},
    "E": {"en": "Fund rules", "th": "กฎเกณฑ์กองทุนรวม"},
}

ROLES = {
    "ic": {"en": "Investment consultant (IC)", "th": "ผู้แนะนำการลงทุน (IC)"},
    "ip": {"en": "Investment planner (IP)", "th": "ผู้วางแผนการลงทุน (IP)"},
    "analyst": {"en": "Investment analyst", "th": "นักวิเคราะห์การลงทุน"},
    "fund_manager": {"en": "Fund manager", "th": "ผู้จัดการกองทุน"},
    "firm": {"en": "Licensed firm (broker, bank, AMC)", "th": "ผู้ประกอบธุรกิจ (บล. ธนาคาร บลจ.)"},
}

REGULATORS = {
    "SEC": {"en": "SEC Thailand", "th": "ก.ล.ต."},
}

STALE_AFTER_DAYS = 183  # entries not checked for about 6 months get a reminder


@dataclass(frozen=True)
class Source:
    code: str        # the document number as written by the regulator, e.g. "ทลธ. 8/2557"
    title: Text
    url: str
    regulator: str = "SEC"


@dataclass(frozen=True)
class Table:
    """A summary table shown above a topic's entries (e.g. which licence may do what)."""
    topic: str
    icon: str
    title: Text
    header: tuple[Text, ...]
    rows: tuple[tuple[Text | bool, ...], ...]  # a bool cell is shown as ✅ / –
    source: Source
    note: Text | None = None                   # e.g. which pages of the source


@dataclass(frozen=True)
class Entry:
    id: str          # e.g. "A01"; stable, so links and progress can point at it
    topic: str       # key of TOPICS
    title: Text
    summary: Text
    points: tuple[Text, ...]
    sources: tuple[Source, ...]
    effective: str   # ISO date the current version took effect ("" if not stated)
    checked: str     # ISO date I last checked it against the source
    roles: tuple[str, ...] = ()
    modules: tuple[int, ...] = ()  # CFP modules it belongs to
    keywords: tuple[str, ...] = field(default=())  # extra words to find it by in search

    def is_stale(self, today: date | None = None) -> bool:
        today = today or date.today()
        return (today - date.fromisoformat(self.checked)).days > STALE_AFTER_DAYS
