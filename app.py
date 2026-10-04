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

st.set_page_config(page_title="CFP Toolkit", page_icon="🧭", layout="wide")

home = st.Page("home.py", title="Home", icon="🏠", default=True)

# Tools used across all modules, shown above the modules in the sidebar.
TOOL_PAGES = [
    st.Page("calculators/financial_calculator.py", title="Financial calculator", icon="🧮",
            url_path="calculator"),
]

# Pages of each module, by module number. Modules without pages show "Coming later".
MODULE_PAGES = {
    2: [
        st.Page("module2_investment/dashboard.py", title="Thai mutual funds", icon="🏦",
                url_path="mutual-funds"),
        st.Page("module2_investment/simulator.py", title="Investment simulator", icon="📈",
                url_path="simulator"),
    ],
}

all_pages = [home] + TOOL_PAGES + [p for pages in MODULE_PAGES.values() for p in pages]
current = st.navigation(all_pages, position="hidden")  # we draw our own menu below

# Sidebar menu: one section per module that opens and closes. The module of the
# page you are on starts open.
with st.sidebar:
    st.page_link(home, icon=home.icon)
    st.caption("TOOLS")
    for p in TOOL_PAGES:
        st.page_link(p, icon=p.icon)
    st.caption("CFP MODULES")
    for m in MODULES:
        pages = MODULE_PAGES.get(m.number, [])
        is_current = any(p.url_path == current.url_path for p in pages)
        with st.expander(f"Module {m.number} · {m.name_en}", expanded=is_current):
            for p in pages:
                st.page_link(p, icon=p.icon)
            if not pages:
                st.caption("Coming later")
    st.divider()

current.run()
