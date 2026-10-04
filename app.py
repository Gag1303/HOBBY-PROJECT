"""CFP Toolkit - a local web app with tools for each CFP module.

Run it with:
    streamlit run app.py
(or double-click run_app.bat). It opens in your browser at http://localhost:8501
and only runs on this computer.

To add a tool for another module, create its folder (e.g. module3_insurance/) with a
page file, then add an st.Page(...) for it to MODULE_PAGES below.
"""

import streamlit as st

from cfp_modules import MODULES
from i18n import lang, language_switcher, t

st.set_page_config(page_title="CFP Toolkit", page_icon="🧭", layout="wide")

home = st.Page("home.py", title=t("Home"), icon="🏠", default=True)

# Tools used across all modules, shown above the modules in the sidebar.
TOOL_PAGES = [
    st.Page("calculators/financial_calculator.py", title=t("Financial calculator"), icon="🧮",
            url_path="calculator"),
]

# Pages of each module, by module number. Modules without pages show "Coming later".
MODULE_PAGES = {
    2: [
        st.Page("module2_investment/dashboard.py", title=t("Thai mutual funds"), icon="🏦",
                url_path="mutual-funds"),
        st.Page("module2_investment/simulator.py", title=t("Investment simulator"), icon="📈",
                url_path="simulator"),
    ],
}

all_pages = [home] + TOOL_PAGES + [p for pages in MODULE_PAGES.values() for p in pages]
current = st.navigation(all_pages, position="hidden")  # we draw our own menu below

# Sidebar menu: language switch, Home, Tools, then one section per module that opens and
# closes. The module of the page you are on starts open.
with st.sidebar:
    language_switcher()
    st.page_link(home, icon=home.icon)
    st.caption(t("TOOLS"))
    for p in TOOL_PAGES:
        st.page_link(p, icon=p.icon)
    st.caption(t("CFP MODULES"))
    for m in MODULES:
        pages = MODULE_PAGES.get(m.number, [])
        is_current = any(p.url_path == current.url_path for p in pages)
        name = m.name_th if lang() == "th" else m.name_en
        with st.expander(t("Module {n}", n=m.number) + f" · {name}", expanded=is_current):
            for p in pages:
                st.page_link(p, icon=p.icon)
            if not pages:
                st.caption(t("Coming later"))
    st.divider()

current.run()
