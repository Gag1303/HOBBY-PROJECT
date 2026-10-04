"""CFP career guide page: path to CFP, ethics, renewal / working abroad, TFPA documents, my progress.

The content is a study summary in career/content.py; the official documents are linked, not copied.
"""

import streamlit as st

import auth
from career.content import (
    AFPT, CROSS_BORDER, DOCUMENTS, ETHICS_PRINCIPLES, FOUR_E, PRACTICE_STEPS, RENEWAL, RULES,
)
from i18n import lang, t
from user_settings import load_settings, save_setting

TH = lang() == "th"


def pick(text: dict) -> str:
    return text["th"] if TH else text["en"]


st.title("🎓 " + t("CFP career guide"))
st.caption(t("A personal study summary of the Thai Financial Planners Association (TFPA) documents. "
             "Rules and fees can change – always check the official documents in the Documents tab."))

tab_path, tab_ethics, tab_renew, tab_docs, tab_me = st.tabs([
    "🧭 " + t("Path to CFP"), "⚖️ " + t("Ethics and rules"), "🔄 " + t("Renewal and working abroad"),
    "📂 " + t("Documents"), "✅ " + t("My progress"),
])

# ---------- path to CFP (4E) ----------

with tab_path:
    st.markdown(t("To use the CFP® mark in Thailand you need all **4 E's**:"))
    cols = st.columns(4)
    for col, e in zip(cols, FOUR_E):
        col.markdown(f"### {e['icon']}\n**{pick(e['title'])}**")
    for e in FOUR_E:
        with st.expander(f"{e['icon']} {pick(e['title'])}", expanded=e["key"] == "education"):
            for p in e["points"]:
                st.markdown(f"- {pick(p)}")
    st.info(pick(AFPT))
    st.markdown("#### " + t("The 6 steps of financial planning (practice standards)"))
    st.markdown("\n".join(f"{i}. {th if TH else en}" for i, (en, th) in enumerate(PRACTICE_STEPS, 1)))

# ---------- ethics ----------

with tab_ethics:
    st.markdown("#### " + t("The 8 principles of the Code of Ethics"))
    for i, (en, th, desc_en, desc_th) in enumerate(ETHICS_PRINCIPLES):
        if i % 2 == 0:
            cols = st.columns(2)  # new row every 2 cards so rows line up
        with cols[i % 2].container(border=True):
            st.markdown(f"**{i + 1}. {th + ' (' + en + ')' if TH else en}**")
            st.caption(desc_th if TH else desc_en)
    st.markdown("#### " + t("Key rules of conduct"))
    st.caption(t("Grouped from the 37 rules of conduct. Breaking them can lead to disciplinary action "
                 "and losing the right to use the CFP mark."))
    for group in RULES:
        with st.expander(pick(group["title"]), expanded=True):
            for item in group["items"]:
                st.markdown(f"- {pick(item)}")

# ---------- renewal and abroad ----------

with tab_renew:
    st.markdown("#### " + t("Keeping your CFP: renewal and CPD"))
    for p in RENEWAL:
        st.markdown(f"- {pick(p)}")
    st.markdown("#### 🌏 " + t("Working in other countries (cross-border certification)"))
    for p in CROSS_BORDER:
        st.markdown(f"- {pick(p)}")

# ---------- documents ----------

with tab_docs:
    st.caption(t("Official documents on the TFPA website. They open on tfpa.or.th."))
    for section_en, section_th, docs in DOCUMENTS:
        st.markdown(f"#### {section_th if TH else section_en}")
        for en, th, url in docs:
            st.markdown(f"- [{th if TH else en}]({url})")

# ---------- my progress (saved on this computer, per account) ----------

with tab_me:
    username = auth.current_user()["username"]
    all_progress = load_settings().get("cfp_progress", {})
    saved = all_progress.get(username, {})
    modules = [t("Module {n}", n=n) for n in range(1, 7)]
    papers = [t("Paper 1"), t("Paper 2"), t("Paper 3"), t("Paper 4 part 1"), t("Paper 4 part 2")]

    st.caption(t("Tick what you have done. It is saved on this computer only, for your account."))
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**📚 " + t("Training done (or exempted)") + "**")
        trained = [st.checkbox(m, value=saved.get("trained", [False] * 6)[i], key=f"cfp_t{i}")
                   for i, m in enumerate(modules)]
    with c2:
        st.markdown("**📝 " + t("Exams passed") + "**")
        passed = [st.checkbox(p, value=saved.get("passed", [False] * 5)[i], key=f"cfp_p{i}")
                  for i, p in enumerate(papers)]
    with c3:
        st.markdown("**💼 " + t("Experience") + "**")
        years = st.number_input(t("Years of qualifying work"), min_value=0.0, max_value=40.0, step=0.5,
                                value=float(saved.get("years", 0.0)), key="cfp_years")
        st.markdown("**⚖️ " + t("Ethics") + "**")
        ethics = st.checkbox(t("I have read the Code of Ethics"), value=saved.get("ethics", False),
                             key="cfp_ethics")

    progress = {"trained": trained, "passed": passed, "years": years, "ethics": ethics}
    if progress != saved:
        save_setting("cfp_progress", {**all_progress, username: progress})

    steps_done = sum(trained) + sum(passed) + min(years, 3) / 3 * 3 + ethics
    st.progress(steps_done / 15, text=t("Overall progress: {pct}", pct=f"{steps_done / 15:.0%}"))

    if all(trained) and all(passed) and years >= 3 and ethics:
        st.success(t("You meet all 4 E's – you can apply for CFP registration on tfpa.or.th."))
    else:
        nxt = next((t("Next: training for {m}", m=m) for m, d in zip(modules, trained) if not d), None) \
            or next((t("Next: pass {p}", p=p) for p, d in zip(papers, passed) if not d), None) \
            or (t("Next: build up 3 years of experience ({left} to go)", left=f"{3 - years:g}")
                if years < 3 else t("Next: read the Code of Ethics (Ethics tab)"))
        st.info(nxt)
    if trained[0] and trained[1] and passed[0] and passed[1]:
        st.caption("🏅 " + t("Modules 1–2 and papers 1–2 done: you may already qualify for AFPT "
                             "(check that your module 2 is the 2021 curriculum)."))
