"""Knowledge page: study notes by CFP module and course chapter, with formulas, worked examples and practice.

A module's "Knowledge for this module" button opens this page with the module filter already set
(through st.session_state["knowledge_module"]).
"""

import streamlit as st

from i18n import lang, t
from knowledge.library import CHAPTERS, CONCEPTS, LOS_URLS, PARTS, covered_los, find, modules_with_concepts
from knowledge.model import TOOLS
from reading.books import BY_ID as BOOKS

TH = lang() == "th"


def pick(text: dict) -> str:
    return text["th"] if TH else text["en"]


def markdown_table(header: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    return "\n".join(lines + ["| " + " | ".join(r) + " |" for r in rows])


st.title("📘 " + t("Knowledge"))
st.caption(t("Study notes for each CFP module, organised by the official course chapters and mapped to the "
             "learning objectives (LOS). My own summary of standard finance theory – check details in the course "
             "text."))

# ---------- filters ----------

ALL = "all"
modules = modules_with_concepts()
if st.session_state.get("knowledge_module") not in modules:
    st.session_state["knowledge_module"] = modules[0]
module_labels = {m: t("Module {n}", n=m) for m in modules}

c1, c2, c3 = st.columns([3, 2, 3])
query = c1.text_input(t("Search"), placeholder=t("e.g. Sharpe, CAPM, ผลตอบแทน"), key="knowledge_query")
module = c2.selectbox(t("CFP module"), modules, format_func=module_labels.get, key="knowledge_module")
chapters = [ch for ch in CHAPTERS if ch.module == module]
chapter_labels = {ALL: t("All chapters"), **{ch.number: f"{ch.number} · {pick(ch.title)}" for ch in chapters}}
if st.session_state.get("knowledge_chapter") not in chapter_labels:
    st.session_state["knowledge_chapter"] = ALL
number = c3.selectbox(t("Chapter"), list(chapter_labels), format_func=chapter_labels.get, key="knowledge_chapter")

results = find(query, module, None if number == ALL else number)

total_los = sum(ch.los_count for ch in chapters)
done_los = sum(len(covered_los(module, ch.number)) for ch in chapters)
m1, m2, m3 = st.columns(3)
m1.metric(t("Concepts shown"), f"{len(results)} / {sum(c.module == module for c in CONCEPTS)}")
m2.metric(t("Chapters started"), f"{sum(bool(covered_los(module, ch.number)) for ch in chapters)} / {len(chapters)}")
m3.metric(t("Learning objectives covered"), f"{done_los} / {total_los}",
          help=t("The official learning outcome statements (LOS) of the module that have a concept here."))

with st.expander("🗺️ " + t("Chapters, exam parts and coverage"), expanded=not query and number == ALL):
    rows = []
    for ch in chapters:
        covered = len(covered_los(module, ch.number))
        status = "✅" if covered == ch.los_count else ("🟡" if covered else "–")
        rows.append([str(ch.number), pick(ch.title), pick(PARTS[module][ch.part]), f"{status} {covered} / {ch.los_count}"])
    st.markdown(markdown_table([t("Chapter"), t("Title"), t("Part"), t("LOS covered")], rows))
    st.caption(t("Source: [TFPA learning objectives for Module {n}]({url}).", n=module, url=LOS_URLS[module]))

# ---------- concepts, grouped by chapter ----------

if not results:
    st.warning(t("No concept matches these filters."))

for ch in chapters:
    concepts = [c for c in results if c.chapter == ch.number]
    if not concepts:
        if number == ch.number:
            st.info(t("This chapter is coming later."))
        continue
    st.markdown(f"### {t('Chapter {n}', n=ch.number)} · {pick(ch.title)}")
    st.caption(pick(PARTS[module][ch.part]))
    for c in concepts:
        with st.container(border=True):
            st.markdown(f"**{c.id} · {pick(c.title)}**")
            st.write(pick(c.summary))
            if c.points:
                st.markdown("\n".join(f"- {pick(p)}" for p in c.points))
            for f in c.formulas:
                st.latex(f.latex)
                st.caption(f"**{pick(f.name)}** – {pick(f.where)}")
            if c.example:
                with st.expander("✏️ " + t("Worked example")):
                    st.write(pick(c.example))
            if c.questions:
                with st.expander("🎯 " + t("Practice ({n})", n=len(c.questions))):
                    for i, q in enumerate(c.questions, 1):
                        st.markdown(f"**{i}.** {pick(q.question)}")
                        with st.popover(t("Show answer")):
                            st.write(pick(q.answer))
            links = [t("LOS {ids}", ids=", ".join(c.los))]
            links += ["📚 " + BOOKS[b].title for b in c.books]
            links += ["⚖️ " + t("Rule {id}", id=r) for r in c.rules]
            links += ["🧮 " + pick(TOOLS[x]) for x in c.tools]
            st.caption("  \n".join(["🎯 " + links[0], *links[1:]]))

coming = [f"{ch.number} · {pick(ch.title)}" for ch in chapters if not covered_los(module, ch.number)]
if coming and not query:
    st.divider()
    st.caption(t("Coming next: {topics}", topics=", ".join(coming)))
