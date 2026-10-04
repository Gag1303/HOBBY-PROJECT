"""Log in screen, or the first-time "create the superadmin" screen when no accounts exist.

Only shown while auth.LOGIN_ENABLED is True. The checks themselves are in auth.py.
"""

import streamlit as st

import auth
from i18n import language_switcher, t

language_switcher()

if not auth.load_users():
    st.title("🔐 " + t("Create the superadmin account"))
    st.write(t("No accounts exist yet. The first account is the superadmin: it sees everything "
               "and decides what other accounts can see."))
    with st.form("setup"):
        username = st.text_input(t("Username")).strip().lower()
        name = st.text_input(t("Display name"))
        password = st.text_input(t("Password"), type="password")
        confirm = st.text_input(t("Password again"), type="password")
        submitted = st.form_submit_button(t("Create account"), type="primary")
    if submitted:
        error = auth.check_username(username, {}) or auth.check_new_password(password, confirm)
        if error:
            st.error(error)
        else:
            auth.create_first_superadmin(username, name, password)
            st.rerun()
else:
    st.title("🔐 " + t("Log in to CFP Toolkit"))
    if message := st.session_state.pop("auth_message", None):
        st.info(message)
    with st.form("login"):
        username = st.text_input(t("Username")).strip().lower()
        password = st.text_input(t("Password"), type="password")
        submitted = st.form_submit_button(t("Log in"), type="primary")
    if submitted:
        result, minutes = auth.try_login(username, password)
        if result == "ok":
            st.rerun()
        elif result == "locked":
            st.error(t("Too many wrong passwords. Try again in {n} minutes.", n=minutes))
        else:
            # Same message whether the username exists or not, so it does not reveal who has an account.
            st.error(t("Wrong username or password."))
