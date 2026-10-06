"""SEC update watcher on screen: the daily auto-check, the panel on the Law & Regulation page and the
Home page banner. The checking itself is in regulation/watcher.py."""

from datetime import date, datetime

import streamlit as st

from i18n import t
from regulation import watcher


def auto_check() -> dict:
    """Check the SEC once a day by itself (the first time a page that shows updates is opened)."""
    state = watcher.load_state()
    if watcher.is_due(state):
        with st.spinner(t("Checking the SEC for new rules…")):
            state = watcher.check()
    return state


def _when(iso: str | None) -> str:
    return datetime.fromisoformat(iso).strftime("%d %b %Y %H:%M") if iso else t("never")


def _line(n: watcher.Notice, affected: list[str]) -> str:
    title = f"[{n.title}]({n.url})" if n.url else n.title
    text = f"**{n.number}** · {date.fromisoformat(n.issued).strftime('%d %b %Y')} – {title}"
    if not n.active:
        text += " · " + t("cancelled")
    if affected:
        text += "  \n" + t("May change: {ids}", ids=", ".join(affected))
    return text


def panel(state: dict) -> None:
    """The "SEC updates" box at the top of the Law & Regulation page."""
    new = watcher.unreviewed(state)
    label = "🔔 " + t("SEC updates") + (f" · {t('{n} new', n=len(new))}" if new else "")
    with st.expander(label, expanded=bool(new or state.get("error"))):
        c1, c2 = st.columns([4, 1])
        c1.caption(t("Last checked {when} · source: [SEC rules issued this year]({url}) · checks by itself "
                     "once a day", when=_when(state.get("last_check")), url=watcher.INDEX_URL))
        if c2.button(t("Check now"), key="sec_check_now", use_container_width=True):
            with st.spinner(t("Checking the SEC for new rules…")):
                state = watcher.check()
            st.rerun()
        if state.get("error"):
            st.warning(t("Couldn't read the SEC website this time – try again later. ({error})",
                         error=state["error"]))
        if new:
            st.markdown(t("New SEC documents that may change rules here. Read them, update the rules if "
                          "needed, then mark them as reviewed."))
            for n in new:
                st.markdown("- 🆕 " + _line(n, [e.id for e in n.related() if n.affects(e)]))
            if st.button(t("Mark all as reviewed"), key="sec_reviewed"):
                watcher.mark_reviewed([n.id for n in new])
                st.rerun()
        elif state.get("last_check"):
            st.success(t("Nothing new: no SEC document since the rules were checked seems to change them."))
        others = [n for n in watcher.relevant(state) if n not in new]
        if others:
            with st.popover(t("All {n} related SEC documents this year", n=len(others)), use_container_width=True):
                st.caption(t("Already reviewed or older than the rules' check dates."))
                for n in others:
                    st.markdown("- " + _line(n, [e.id for e in n.related()]))


def home_banner(state: dict) -> None:
    new = watcher.unreviewed(state)
    if new:
        st.info("🔔 " + t("{n} new SEC documents may change your Law & Regulation rules.", n=len(new)))
        st.page_link("interface/regulation/bible.py", label=t("See the SEC updates"), icon="⚖️")
