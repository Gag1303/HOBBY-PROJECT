"""Home page: overview of the 6 Thai CFP modules and which tools exist for each."""

import streamlit as st

import auth
from cfp_modules import MODULES
from i18n import lang, t

st.title("🧭 " + t("CFP Toolkit"))
st.write(t("Personal practice tools, organised by the 6 modules of the Thai CFP® program. "
           "Each module gets its own tools as I learn it."))

user = auth.current_user()
if auth.can(user, "tools") or auth.can(user, "career"):
    with st.container(border=True):
        st.markdown(t("**Tools** · for every module"))
        if auth.can(user, "tools"):
            st.page_link("interface/calculators/financial_calculator.py",
                         label=t("Financial calculator: TVM, NPV / IRR, interest rate conversion"),
                         icon="🧮")
        if auth.can(user, "career"):
            st.page_link("interface/career/guide.py",
                         label=t("CFP career guide: path to CFP, ethics, renewal, working abroad, "
                                 "TFPA documents"), icon="🎓")

visible = [m for m in MODULES if auth.can(user, f"m{m.number}")]
if not visible and not (auth.can(user, "tools") or auth.can(user, "career")):
    st.info(t("Your account cannot see any area yet. Ask the superadmin to give you access."))

for i, m in enumerate(visible):
    if i % 3 == 0:
        cols = st.columns(3)  # new row every 3 cards so rows line up
    title, other = (m.name_th, m.name_en) if lang() == "th" else (m.name_en, m.name_th)
    with cols[i % 3].container(border=True):
        st.markdown(f"**{t('Module {n}', n=m.number)}**  \n### {title}")
        st.caption(other)
        st.write(t(m.description))
        if m.home_page:
            st.page_link(m.home_page, label=t("Open"), icon="➡️")
        else:
            st.markdown(":gray[" + t("Coming later") + "]")

st.caption(t("For personal learning only. Not financial advice, and the data sources used here "
             "do not allow commercial use."))
