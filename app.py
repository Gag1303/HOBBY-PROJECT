"""CFP Toolkit - a local web app with tools for each CFP module.

Run it with:
    streamlit run app.py
(or double-click run_app.bat). It opens in your browser at http://localhost:8501
and only runs on this computer.

To add a tool for another module, create its folder (e.g. module3_insurance/) with a
page file, then add an st.Page(...) line for it below.
"""

import streamlit as st

st.set_page_config(page_title="CFP Toolkit", page_icon="🧭", layout="wide")

pages = {
    "": [
        st.Page("home.py", title="Home", icon="🏠", default=True),
    ],
    "Module 2 · Investment planning": [
        st.Page("module2_investment/dashboard.py", title="Thai mutual funds", icon="📈",
                url_path="mutual-funds"),
    ],
}

st.navigation(pages).run()
