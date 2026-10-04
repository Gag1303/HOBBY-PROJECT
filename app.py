"""CFP Toolkit - a local web app with tools for each CFP module.

Run it with:
    streamlit run app.py
(or double-click run_app.bat). It opens in your browser at http://localhost:8501
and only runs on this computer.

Everything you see (pages, sidebar menu, login screen) is in the interface/ folder.
The logic behind it (fund data, calculations, accounts, translations) stays outside it.
"""

import streamlit as st

from interface import navigation

st.set_page_config(page_title="CFP Toolkit", page_icon="🧭", layout="wide")

navigation.run()
