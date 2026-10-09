"""Law & Regulation page: search and filter the rules in regulation/, with sources and check dates.

A module's "Rules for this module" button opens this page with the module filter already set
(through st.session_state["law_module"]).
"""

from datetime import date

import streamlit as st

from cfp_modules import MODULES
from edition import OFFLINE
from i18n import lang, t
from interface.regulation import sec_updates
from regulation.library import ENTRIES, TABLES, find, modules_with_entries
from regulation.model import ROLES, TOPICS
from regulation.watcher import flags

TH = lang() == "th"


def pick(text: dict) -> str:
    return text["th"] if TH else text["en"]


def markdown_table(header: list[str], rows: list[list[str]]) -> str:
    """A simple table whose long cells wrap (st.dataframe would cut them off)."""
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    return "\n".join(lines + ["| " + " | ".join(r) + " |" for r in rows])


def nice_date(iso: str) -> str:
    return date.fromisoformat(iso).strftime("%d %b %Y")


st.title("⚖️ " + t("Law & Regulation"))
st.caption(t("A personal study reference: rules summarised in my own words, each linked to the official "
             "document. Not legal advice – the official document is what counts, and rules change."))

if OFFLINE:
    st.caption("🔗 " + t("Links to websites don't open in the Offline Edition – open them from the normal app, or search the title on the website."))

# ---------- filters ----------

ALL = "all"
modules = modules_with_entries()
if st.session_state.get("law_module") not in [ALL, *modules]:
    st.session_state["law_module"] = ALL

topic_labels = {ALL: t("All topics"), **{k: f"{k} · {pick(v)}" for k, v in TOPICS.items()}}
module_labels = {ALL: t("All modules"), **{m: t("Module {n}", n=m) for m in modules}}
role_labels = {ALL: t("All roles"), **{k: pick(v) for k, v in ROLES.items()}}

c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
query = c1.text_input(t("Search"), placeholder=t("e.g. renew, CFP, ESG, ต่ออายุ"), key="law_query")
topic = c2.selectbox(t("Topic"), list(topic_labels), format_func=topic_labels.get, key="law_topic")
module = c3.selectbox(t("CFP module"), list(module_labels), format_func=module_labels.get, key="law_module")
role = c4.selectbox(t("Role"), list(role_labels), format_func=role_labels.get, key="law_role")

results = find(query, None if topic == ALL else topic, None if module == ALL else module,
               None if role == ALL else role)

watch = {} if OFFLINE else sec_updates.auto_check()  # the Offline Edition can't reach the SEC
flagged = {} if OFFLINE else flags(watch)
stale = [e for e in ENTRIES if e.is_stale() or e.id in flagged]
m1, m2, m3 = st.columns(3)
m1.metric(t("Rules shown"), f"{len(results)} / {len(ENTRIES)}")
m2.metric(t("Last checked"), nice_date(max(e.checked for e in ENTRIES)))
m3.metric(t("Need re-checking"), len(stale),
          help=t("Rules not checked against their source for 6 months, or that a newer SEC document may change."))
if not OFFLINE:
    sec_updates.panel(watch)

if module != ALL:
    m = MODULES[module - 1]
    st.info(t("Showing rules for Module {n} · {name}", n=module, name=m.name_th if TH else m.name_en))

# ---------- summary tables of the topics in view (hidden while searching) ----------

if not query:
    shown_topics = {e.topic for e in results}
    for tb in TABLES:
        if tb.topic not in shown_topics:
            continue
        with st.expander(f"{tb.icon} {pick(tb.title)}", expanded=topic == tb.topic):
            st.markdown(markdown_table(
                [pick(h) for h in tb.header],
                [[("✅" if c else "–") if isinstance(c, bool) else pick(c) for c in row] for row in tb.rows]))
            note = f" ({pick(tb.note)})" if tb.note else ""
            st.caption(t("Source: {src}", src=tb.source.code) + " · " + pick(tb.source.title) + note)

# ---------- entries, grouped by topic ----------

if not results:
    st.warning(t("No rule matches these filters."))

for key, name in TOPICS.items():
    entries = [e for e in results if e.topic == key]
    if not entries:
        if topic == key:
            st.info(t("This topic is coming later."))
        continue
    st.markdown(f"### {key} · {pick(name)}")
    for e in entries:
        with st.container(border=True):
            st.markdown(f"**{e.id} · {pick(e.title)}**" + ("  ⚠️" if e.is_stale() else ""))
            st.write(pick(e.summary))
            if e.points:
                st.markdown("\n".join(f"- {pick(p)}" for p in e.points))
            links = " · ".join(f"[{s.code} – {pick(s.title)}]({s.url})" for s in e.sources)
            when = t("checked {d}", d=nice_date(e.checked))
            if e.effective:
                when = t("in force since {d}", d=nice_date(e.effective)) + " · " + when
            tags = ", ".join([t("Module {n}", n=m) for m in e.modules] + [pick(ROLES[r]) for r in e.roles])
            st.caption(f"📄 {links}  \n🗓️ {when}  \n🏷️ {tags}")
            if e.is_stale():
                st.warning(t("Not checked for over 6 months – compare it with the source before relying on it."))
            for n in flagged.get(e.id, []):
                st.warning("🔔 " + t("A newer SEC document may change this rule: {doc} – re-check it.",
                                     doc=f"[{n.number}]({n.url})" if n.url else n.number))

coming = [f"{k} · {pick(v)}" for k, v in TOPICS.items() if not any(e.topic == k for e in ENTRIES)]
if coming:
    st.divider()
    st.caption(t("Coming next: {topics}", topics=", ".join(coming)))
