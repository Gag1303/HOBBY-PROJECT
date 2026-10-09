"""CFP reading list page: Maruey Library books by module, my reading notes and practice questions.

A module's "Books for this module" button opens this page with the module filter already set
(through st.session_state["reading_module"]).
"""

import streamlit as st

import auth
from cfp_modules import MODULES
from edition import OFFLINE
from i18n import lang, t
from reading import notes
from reading.books import BOOKS, BY_ID, CATALOG_CHECKED, MARUEY

TH = lang() == "th"
USER = auth.current_user()["username"]
STATUS_LABELS = {"to_read": "📋 " + t("To read"), "reading": "📖 " + t("Reading"), "done": "✅ " + t("Done")}
KIND_LABELS = {"book": "📕 " + t("Borrow the book"), "ebook": "📱 " + t("Borrow the eBook")}


def pick(text: dict) -> str:
    return text["th"] if TH else text["en"]


def module_name(n: int) -> str:
    m = MODULES[n - 1]
    return t("Module {n}", n=n) + " · " + (m.name_th if TH else m.name_en)


def book_label(book_id: str) -> str:
    b = BY_ID[book_id]
    return f"{t('Module {n}', n=b.module)} · {b.title}"


st.title("📚 " + t("CFP reading list"))
st.caption(t("Books to borrow from the [Maruey Library]({url}) (SET), chosen for each CFP module, with my own "
             "notes and practice questions. Only the catalog details are here – borrow the book to read it. "
             "Catalog checked {date}.", url=MARUEY, date=CATALOG_CHECKED))

if OFFLINE:
    st.caption("🔗 " + t("Links to websites don't open in the Offline Edition – open them from the normal app, or search the title on the website."))

mine = notes.load(USER)
ALL = "all"
if st.session_state.get("reading_module") not in [ALL, *range(1, 7)]:
    st.session_state["reading_module"] = ALL
module_labels = {ALL: t("All modules"), **{n: module_name(n) for n in range(1, 7)}}
module = st.selectbox(t("CFP module"), list(module_labels), format_func=module_labels.get, key="reading_module")
shown = [b for b in BOOKS if module == ALL or b.module == module]

done = sum(mine["status"].get(b.id) == "done" for b in shown)
shown_ids = {b.id for b in shown}
c1, c2, c3 = st.columns(3)
c1.metric(t("Books read"), f"{done} / {len(shown)}")
c2.metric(t("My notes"), sum(n["book"] in shown_ids for n in mine["notes"]))
c3.metric(t("Practice questions"), len(notes.cards(mine, shown_ids)))

tab_list, tab_notes, tab_practice = st.tabs(["📚 " + t("Reading list"), "📝 " + t("My notes"), "🎯 " + t("Practice")])

# ---------- reading list ----------

with tab_list:
    with st.expander("ℹ️ " + t("How to borrow from Maruey")):
        st.markdown(t(
            "- **Free Trial Member** (sign up as a SET Member): borrow some eBook categories, 5 at a time, for 3 days.\n"
            "- **eBook Member** (200 baht/year): all eBooks, 5 at a time, for 3 days.\n"
            "- **Member** (250 baht/year + 500 baht deposit): printed books too, 7 days, at the SET building.\n"
            "- Don't let others use your membership. Fees and rules as in Maruey's terms – check them on the site."))
    for n in range(1, 7):
        books = [b for b in shown if b.module == n]
        if not books:
            continue
        st.markdown(f"### {module_name(n)}")
        for b in books:
            with st.container(border=True):
                left, right = st.columns([4, 1])
                left.markdown(f"**{b.title}**" + ("  ⭐ " + t("Official CFP course text") if b.core else ""))
                details = [b.author, b.publisher] + ([t("{n} pages", n=b.pages)] if b.pages else []) + \
                          ([t("call no. {c}", c=b.call_no)] if b.call_no else [])
                left.caption(" · ".join(d for d in details if d) + (" · EN" if b.lang == "en" else ""))
                left.write(pick(b.note))
                left.markdown(" · ".join(f"[{KIND_LABELS[kind]}]({url})" for kind, url in b.links))
                status = mine["status"].get(b.id, "to_read")
                new = right.selectbox(t("Status"), notes.STATUSES, index=notes.STATUSES.index(status),
                                      format_func=STATUS_LABELS.get, key=f"status_{b.id}", label_visibility="collapsed")
                if new != status:
                    notes.set_status(USER, b.id, new)
                    st.rerun()
                count = len(notes.notes_for(mine, b.id))
                if count:
                    right.caption(t("{n} notes", n=count))

# ---------- my notes ----------

def card_editor(key: str, cards: list[dict]):
    return st.data_editor(cards or [{"q": "", "a": ""}], num_rows="dynamic", use_container_width=True, key=key,
                          column_config={"q": st.column_config.TextColumn(t("Question"), width="large"),
                                         "a": st.column_config.TextColumn(t("Answer"), width="large")})


def note_form(key: str, book_id: str, note: dict | None = None) -> None:
    note = note or {}
    with st.form(key, clear_on_submit=not note):
        page = st.text_input(t("Page or chapter"), value=note.get("page", ""), placeholder=t("e.g. p. 45 or chapter 3"))
        summary = st.text_area(t("Summary in my own words"), value=note.get("summary", ""), height=150)
        quote = st.text_area(t("Short quote (optional, up to {n} characters)", n=notes.QUOTE_LIMIT),
                             value=note.get("quote", ""), max_chars=notes.QUOTE_LIMIT, height=80)
        st.caption(t("Practice questions from this part (optional) – add rows with the + below the table."))
        cards = card_editor(f"{key}_cards", note.get("cards", []))
        if st.form_submit_button(t("Save note"), type="primary"):
            problems = notes.check(summary, quote)
            if problems:
                for p in problems:
                    st.error(t(p))
            else:
                notes.save_note(USER, book_id, page, summary, quote, list(cards), note.get("id"))
                st.toast(t("Note saved."))
                st.rerun()


with tab_notes:
    st.caption(t("Read the book, then write what you learned in your own words. Short quotes only – it keeps "
                 "the notes yours and helps you remember. Notes are saved on this computer only."))
    book_labels = {b.id: book_label(b.id) for b in shown}
    book_id = st.selectbox(t("Book"), list(book_labels), format_func=book_labels.get, key="notes_book")
    if book_id:
        for nt in notes.notes_for(mine, book_id):
            title = (nt["page"] + " · " if nt["page"] else "") + nt["summary"][:60] + ("…" if len(nt["summary"]) > 60 else "")
            with st.expander("📝 " + title):
                st.markdown(nt["summary"])
                if nt["quote"]:
                    st.markdown(f"> {nt['quote']}")
                for c in nt["cards"]:
                    st.markdown(f"- **{t('Q')}:** {c['q']}  \n  **{t('A')}:** {c['a']}")
                with st.popover("✏️ " + t("Edit")):
                    note_form(f"edit_{nt['id']}", book_id, nt)
                if st.button("🗑️ " + t("Delete note"), key=f"del_{nt['id']}"):
                    notes.delete_note(USER, nt["id"])
                    st.rerun()
        st.markdown("#### " + t("Add a note"))
        note_form(f"new_{book_id}", book_id)

# ---------- practice ----------

with tab_practice:
    deck = notes.cards(mine, shown_ids)
    if not deck:
        st.info(t("No practice questions yet. Add some to your notes in the “My notes” tab."))
    else:
        card = st.session_state.get("practice_card")
        if card not in deck:
            card = st.session_state["practice_card"] = notes.draw(deck)
            st.session_state["practice_show"] = False
        with st.container(border=True):
            st.caption(book_label(card["book"]) + (f" · {card['page']}" if card["page"] else ""))
            st.markdown(f"### {card['q']}")
            if st.session_state.get("practice_show"):
                st.success(card["a"])
        c1, c2 = st.columns(2)
        if c1.button(t("Show answer"), use_container_width=True, disabled=st.session_state.get("practice_show", False)):
            st.session_state["practice_show"] = True
            st.rerun()
        if c2.button(t("Next question"), use_container_width=True, type="primary"):
            st.session_state["practice_card"] = notes.draw(deck, avoid=card)
            st.session_state["practice_show"] = False
            st.rerun()
        st.caption(t("{n} questions in this deck.", n=len(deck)))
