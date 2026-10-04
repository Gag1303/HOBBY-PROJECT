"""My account: who I am, what I can see, change my password."""

import streamlit as st

import auth
from i18n import t

me = auth.current_user()
users = auth.load_users()

st.title("👤 " + t("My account"))
st.markdown(f"**{t('Username')}:** {me['username']}  \n**{t('Display name')}:** {me['name']}  \n"
            f"**{t('Role')}:** {me['role']}")
if auth.is_superadmin(me):
    st.caption(t("Superadmin: you can see everything and manage accounts on the Admin page."))
else:
    st.markdown("**" + t("You can see") + ":**")
    st.markdown("\n".join(f"- {auth.area_label(a)}" for a in me.get("areas", [])) or "–")

st.markdown("#### " + t("Change password"))
with st.form("change_password", clear_on_submit=True):
    current = st.text_input(t("Current password"), type="password")
    password = st.text_input(t("New password"), type="password")
    confirm = st.text_input(t("Password again"), type="password")
    if st.form_submit_button(t("Change password"), type="primary"):
        record = users[me["username"]]
        error = (None if auth.password_ok(record, current) else t("The current password is wrong.")) \
            or auth.check_new_password(password, confirm)
        if error:
            st.error(error)
        else:
            auth.set_password(record, password)
            auth.save_users(users)
            st.success(t("Password changed."))
