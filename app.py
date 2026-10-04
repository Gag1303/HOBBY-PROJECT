"""CFP Toolkit - a local web app with tools for each CFP module.

Run it with:
    streamlit run app.py
(or double-click run_app.bat). It opens in your browser at http://localhost:8501
and only runs on this computer.

Everyone has to log in (see auth.py). The first time, the app asks you to create the superadmin
account. Each page belongs to an area ('tools', 'career', 'm1' ... 'm6'); an account only gets
the pages of the areas it may see, and the superadmin also gets the Admin page.

To add a tool for another module, create its folder (e.g. module3_insurance/) with a
page file, then add an st.Page(...) for it to MODULE_PAGES below.
"""

import streamlit as st

import auth
from cfp_modules import MODULES
from i18n import lang, language_switcher, t

st.set_page_config(page_title="CFP Toolkit", page_icon="🧭", layout="wide")

user = auth.current_user()
if user is None:
    # Not logged in: the login page is the only page, whatever URL was typed.
    st.navigation([st.Page(auth.login_page, title=t("Log in"), icon="🔐")], position="hidden").run()
    st.stop()

home = st.Page("home.py", title=t("Home"), icon="🏠", default=True)
my_account = st.Page("admin/account.py", title=t("My account"), icon="👤", url_path="account")
admin = st.Page("admin/users.py", title=t("Accounts and access"), icon="🛡️", url_path="admin")

# Tools used across all modules, shown above the modules in the sidebar.
TOOL_PAGES = [
    st.Page("calculators/financial_calculator.py", title=t("Financial calculator"), icon="🧮",
            url_path="calculator"),
]

# Guides for the CFP career itself (not one module).
CAREER_PAGES = [
    st.Page("career/guide.py", title=t("CFP career guide"), icon="🎓", url_path="career"),
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

# Only the pages this account may see exist for it; the others cannot be opened at all.
tools = TOOL_PAGES if auth.can(user, "tools") else []
career = CAREER_PAGES if auth.can(user, "career") else []
modules = {m.number: MODULE_PAGES.get(m.number, []) for m in MODULES if auth.can(user, f"m{m.number}")}
admin_pages = [admin] if auth.is_superadmin(user) else []

all_pages = [home, my_account] + admin_pages + tools + career + [p for ps in modules.values() for p in ps]
current = st.navigation(all_pages, position="hidden")  # we draw our own menu below

# Sidebar menu: account, language switch, Home, Tools, Career, then one section per module that
# opens and closes. The module of the page you are on starts open.
with st.sidebar:
    c1, c2 = st.columns([3, 2])
    c1.markdown(f"👤 **{user['name']}**  \n:gray[{user['role']}]")
    if c2.button(t("Log out"), use_container_width=True):
        auth.logout()
        st.rerun()
    language_switcher()
    st.page_link(home, icon=home.icon)
    st.page_link(my_account, icon=my_account.icon)
    if admin_pages:
        st.caption(t("ADMIN"))
        st.page_link(admin, icon=admin.icon)
    if tools:
        st.caption(t("TOOLS"))
        for p in tools:
            st.page_link(p, icon=p.icon)
    if career:
        st.caption(t("CAREER"))
        for p in career:
            st.page_link(p, icon=p.icon)
    if modules:
        st.caption(t("CFP MODULES"))
    for m in MODULES:
        if m.number not in modules:
            continue
        pages = modules[m.number]
        is_current = any(p.url_path == current.url_path for p in pages)
        name = m.name_th if lang() == "th" else m.name_en
        with st.expander(t("Module {n}", n=m.number) + f" · {name}", expanded=is_current):
            for p in pages:
                st.page_link(p, icon=p.icon)
            if not pages:
                st.caption(t("Coming later"))
    st.divider()

current.run()
