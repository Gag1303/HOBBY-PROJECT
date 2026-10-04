"""Admin page (superadmin only): add accounts, choose what each one can see, disable, delete."""

import pandas as pd
import streamlit as st

import auth
from i18n import t
from user_settings import load_settings, save_setting

me = auth.current_user()
if not auth.is_superadmin(me):  # navigation.py already hides this page; double check anyway
    st.error(t("Only a superadmin can open this page."))
    st.stop()

ROLE_LABELS = {"superadmin": t("Superadmin – sees everything, manages accounts"),
               "user": t("User – sees only the areas ticked below")}

st.title("🛡️ " + t("Accounts and access"))
st.caption(t("Accounts are saved on this computer only (users.json, never uploaded to GitHub). "
             "Changes apply on that person's next click."))

if message := st.session_state.pop("admin_message", None):
    st.success(message)

users = auth.load_users()


def done(message: str) -> None:
    auth.save_users(users)
    st.session_state["admin_message"] = message
    st.rerun()


st.dataframe(pd.DataFrame([{
    t("Username"): u,
    t("Display name"): r["name"],
    t("Role"): r["role"],
    t("Can see"): t("Everything") if r["role"] == "superadmin"
    else ", ".join(auth.area_label(a) for a in r.get("areas", [])) or "–",
    t("Status"): t("Disabled") if r.get("disabled") else t("Active"),
    t("Created"): r.get("created", ""),
} for u, r in users.items()]), hide_index=True, use_container_width=True)

tab_add, tab_edit, tab_delete = st.tabs(["➕ " + t("Add account"), "✏️ " + t("Edit account"),
                                         "🗑️ " + t("Delete account")])

with tab_add:
    with st.form("add_user", clear_on_submit=True):
        c1, c2 = st.columns(2)
        username = c1.text_input(t("Username")).strip().lower()
        name = c2.text_input(t("Display name"))
        role = st.radio(t("Role"), auth.ROLES, index=1, format_func=ROLE_LABELS.get)
        areas = st.multiselect(t("Can see (for role User)"), auth.AREAS, default=["tools", "career"],
                               format_func=auth.area_label)
        c1, c2 = st.columns(2)
        password = c1.text_input(t("Password"), type="password")
        confirm = c2.text_input(t("Password again"), type="password")
        if st.form_submit_button(t("Add account"), type="primary"):
            error = auth.check_username(username, users) or auth.check_new_password(password, confirm)
            if error:
                st.error(error)
            else:
                users[username] = auth.new_account(name.strip() or username, role, areas, password)
                done(t("Account {u} added.", u=username))

with tab_edit:
    who = st.selectbox(t("Account"), list(users), key="edit_who")
    if who is None:  # no accounts yet; the Delete tab has nothing to show either
        st.caption(t("There is no account yet."))
        st.stop()
    r = users[who]
    with st.form(f"edit_user_{who}"):  # one form per account, so its fields reload on switch
        name = st.text_input(t("Display name"), value=r["name"])
        role = st.radio(t("Role"), auth.ROLES, index=auth.ROLES.index(r["role"]),
                        format_func=ROLE_LABELS.get)
        areas = st.multiselect(t("Can see (for role User)"), auth.AREAS,
                               default=[a for a in r.get("areas", []) if a in auth.AREAS],
                               format_func=auth.area_label)
        active = st.toggle(t("Account active (can log in)"), value=not r.get("disabled"))
        c1, c2 = st.columns(2)
        password = c1.text_input(t("New password (leave empty to keep)"), type="password")
        confirm = c2.text_input(t("Password again"), type="password")
        if st.form_submit_button(t("Save changes"), type="primary"):
            others = [u for u in auth.active_superadmins(users) if u != who]
            error = None
            if (role != "superadmin" or not active) and not others:
                error = t("This is the only active superadmin. Make another superadmin first.")
            elif who == me["username"] and not active:
                error = t("You cannot disable your own account.")
            elif password:
                error = auth.check_new_password(password, confirm)
            if error:
                st.error(error)
            else:
                r.update(name=name.strip() or who, role=role, areas=areas, disabled=not active)
                if password:
                    auth.set_password(r, password)
                done(t("Account {u} saved.", u=who))

with tab_delete:
    deletable = [u for u in users if u != me["username"]]
    if not deletable:
        st.caption(t("There is no other account to delete."))
    else:
        who = st.selectbox(t("Account"), deletable, key="delete_who")
        sure = st.checkbox(t("Yes, delete {u} and their saved progress. This cannot be undone.", u=who))
        if st.button(t("Delete account"), type="primary", disabled=not sure):
            del users[who]
            progress = load_settings().get("cfp_progress", {})
            if who in progress:
                save_setting("cfp_progress", {u: p for u, p in progress.items() if u != who})
            done(t("Account {u} deleted.", u=who))
