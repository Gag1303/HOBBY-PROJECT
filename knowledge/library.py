"""All Knowledge concepts in one list, with search, chapter coverage and a self-check.

Run `python -m knowledge.library` to check every concept has its texts, valid chapter, learning objectives
and links.
"""

from knowledge import m2_ch02, module2
from knowledge.model import TOOLS, Chapter, Concept

_CHAPTER_FILES = (m2_ch02,)  # add each chapter file here as it is written
CONCEPTS: list[Concept] = [c for f in _CHAPTER_FILES for c in f.CONCEPTS]
CHAPTERS: list[Chapter] = list(module2.CHAPTERS)
PARTS = {2: module2.PARTS}
LOS_URLS = {2: module2.LOS_URL}


def chapter(module: int, number: int) -> Chapter | None:
    return next((c for c in CHAPTERS if c.module == module and c.number == number), None)


def modules_with_concepts() -> list[int]:
    return sorted({c.module for c in CONCEPTS})


def covered_los(module: int, number: int) -> set[str]:
    return {los for c in CONCEPTS if c.module == module and c.chapter == number for los in c.los}


def _haystack(c: Concept) -> str:
    texts = [c.id, *c.keywords, *c.title.values(), *c.summary.values()]
    texts += [t for p in c.points for t in p.values()]
    texts += [t for f in c.formulas for t in (*f.name.values(), *f.where.values())]
    return " ".join(texts).lower()


def find(query: str = "", module: int | None = None, number: int | None = None) -> list[Concept]:
    """Concepts matching all filters; every word of `query` must appear (English or Thai)."""
    words = query.lower().split()
    return [c for c in CONCEPTS
            if (module is None or c.module == module) and (number is None or c.chapter == number)
            and all(w in _haystack(c) for w in words)]


def problems() -> list[str]:
    """Things to fix (empty list = all good)."""
    from reading.books import BY_ID
    from regulation.library import ENTRIES

    rule_ids = {e.id for e in ENTRIES}
    found, seen = [], set()
    for c in CONCEPTS:
        where = f"{c.id}:"
        if c.id in seen:
            found.append(f"{where} duplicate id")
        seen.add(c.id)
        if not c.id.startswith(f"K{c.module}-{c.chapter:02d}-"):
            found.append(f"{where} id does not match module {c.module} chapter {c.chapter}")
        ch = chapter(c.module, c.chapter)
        if ch is None:
            found.append(f"{where} unknown chapter")
        texts = [c.title, c.summary, *c.points, *(f.name for f in c.formulas), *(f.where for f in c.formulas)]
        texts += [q.question for q in c.questions] + [q.answer for q in c.questions] + ([c.example] if c.example else [])
        found += [f"{where} text missing English or Thai: {x}" for x in texts if not (x.get("en") and x.get("th"))]
        found += [f"{where} empty formula" for f in c.formulas if not f.latex.strip()]
        if not c.los:
            found.append(f"{where} no learning objective")
        for los in c.los:
            major, _, minor = los.partition(".")
            if major != str(c.chapter) or not minor.isdigit() or (ch and int(minor) > ch.los_count):
                found.append(f"{where} LOS {los} is not in chapter {c.chapter}")
        found += [f"{where} unknown book {b}" for b in c.books if b not in BY_ID]
        found += [f"{where} unknown rule {r}" for r in c.rules if r not in rule_ids]
        found += [f"{where} unknown tool {x}" for x in c.tools if x not in TOOLS]
        if not c.questions:
            found.append(f"{where} no practice question")
    return found


if __name__ == "__main__":
    issues = problems()
    print(f"{len(CONCEPTS)} concepts, {len(issues)} problems")
    for ch in CHAPTERS:
        print(f"  M{ch.module} ch {ch.number}: {len(covered_los(ch.module, ch.number))}/{ch.los_count} LOS covered")
    print("\n".join(issues))
