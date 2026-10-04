"""Which pages exist and the sidebar menu. app.py calls run() on every page view.

Log in is switched off for now (auth.LOGIN_ENABLED = False): the app opens straight in.
When it is switched on, everyone has to log in (see auth.py). The first time, the app asks you
to create the superadmin account. Each page belongs to an area ('tools', 'career', 'm1' ... 'm6');
an account only gets the pages of the areas it may see, and the superadmin also gets the Admin page.

Page paths are relative to app.py (the project folder), so they all start with "interface/".
To add a page, put its file in interface/ and add an st.Page(...) for it below.
"""

import streamlit as st

import auth
from cfp_modules import MODULES
from i18n import lang, language_switcher, t


def run() -> None:
    user = auth.current_user()
    if user is None:
        # Not logged in: the login page is the only page, whatever URL was typed.
        st.navigation([st.Page("interface/login.py", title=t("Log in"), icon="🔐", url_path="login")],
                      position="hidden").run()
        return

    home = st.Page("interface/home.py", title=t("Home"), icon="🏠", default=True)
    my_account = st.Page("interface/admin/account.py", title=t("My account"), icon="👤",
                         url_path="account")
    admin = st.Page("interface/admin/users.py", title=t("Accounts and access"), icon="🛡️",
                    url_path="admin")

    # Tools used across all modules, shown above the modules in the sidebar.
    tool_pages = [
        st.Page("interface/calculators/financial_calculator.py", title=t("Financial calculator"),
                icon="🧮", url_path="calculator"),
    ]

    # Guides for the CFP career itself (not one module).
    career_pages = [
        st.Page("interface/career/guide.py", title=t("CFP career guide"), icon="🎓", url_path="career"),
    ]

    # Pages of each module, by module number. Modules without pages show "Coming later".
    module_pages = {
        2: [
            st.Page("interface/module2_investment/dashboard.py", title=t("Thai mutual funds"),
                    icon="🏦", url_path="mutual-funds"),
            st.Page("interface/module2_investment/simulator.py", title=t("Investment simulator"),
                    icon="📈", url_path="simulator"),
        ],
    }

    # Only the pages this account may see exist for it; the others cannot be opened at all.
    tools = tool_pages if auth.can(user, "tools") else []
    career = career_pages if auth.can(user, "career") else []
    modules = {m.number: module_pages.get(m.number, []) for m in MODULES if auth.can(user, f"m{m.number}")}
    admin_pages = [admin] if auth.LOGIN_ENABLED and auth.is_superadmin(user) else []
    account_pages = [my_account] if auth.LOGIN_ENABLED else []

    all_pages = [home] + account_pages + admin_pages + tools + career + [p for ps in modules.values() for p in ps]
    current = st.navigation(all_pages, position="hidden")  # we draw our own menu below

    # Sidebar menu: account, language switch, Home, Tools, Career, then one section per module that
    # opens and closes. The module of the page you are on starts open.
    with st.sidebar:
        if auth.LOGIN_ENABLED:
            c1, c2 = st.columns([3, 2])
            c1.markdown(f"👤 **{user['name']}**  \n:gray[{user['role']}]")
            if c2.button(t("Log out"), use_container_width=True):
                auth.logout()
                st.rerun()
        language_switcher()
        st.page_link(home, icon=home.icon)
        for p in account_pages:
            st.page_link(p, icon=p.icon)
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
