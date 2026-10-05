# HOBBY-PROJECT
IF 1 DAY I HAVE TO MANAGE ALL FINANCIAL THING

## CFP Toolkit
Personal practice tools, organised by the 6 modules of the Thai CFP® program.

| Module | Topic | Tools | Folder |
|---|---|---|---|
| 1 | Foundation of financial planning, tax and ethics | – | – |
| 2 | Investment planning | Thai mutual fund dashboard, investment simulator (Lump sum / DCA / VCA), data downloader | [module2_investment/](module2_investment/) |
| 3 | Insurance planning | – | – |
| 4 | Retirement planning | – | – |
| 5 | Tax & estate planning | – | – |
| 6 | Financial plan construction | – | – |

**CFP career guide** ([career/](career/)): path to CFP (the 4 E's: education, exam, experience,
ethics), the code of ethics and key rules of conduct, renewal/CPD, cross-border certification for
working abroad, links to TFPA's official documents, and a personal progress tracker. It is a study
summary in my own words; the TFPA documents themselves are not stored in this repo.

**Tools for every module** ([calculators/](calculators/)): financial calculator like the HP 10bII /
Casio FC-200V: TVM (N, I/Y, PV, PMT, FV with P/Y, C/Y, BGN/END and a schedule), cash flows
(NPV / IRR) and interest rate conversion (nominal ↔ effective).

## Setup
```
pip install -r requirements.txt
```

## Run the app (only on this computer)
Double-click `run_app.bat`, or run:
```
streamlit run app.py
```
It opens at http://localhost:8501. Switch between **English | ไทย** at the top of the sidebar;
the choice is saved in `user_settings.json` (not uploaded to GitHub), so it stays after a
refresh or restart. The home page shows all 6 modules. In the sidebar each module
is a section you can open and close; the module of the page you are on opens by itself.

### Law & Regulation (the "Bible")
Sidebar → **REFERENCE → Law & Regulation**: SEC rules summarised in my own words (English and
Thai), each with its official source link, the date it took effect and the date I last checked it.
Search and filter by topic, CFP module and role; each CFP module in the sidebar has a
**Rules for this module** button that opens the page already filtered. Entries not checked for
6 months are flagged. Done: A (licences & career path), B (conduct with clients) and C (penalties);
D (fund structure) and E (fund rules) come next. The SEC PDFs I read are kept only in
`data/sec/` (not uploaded). Run `python -m regulation.library` to check every entry has its texts,
sources and dates. This is a study reference, not legal advice.

### Accounts and access
**Switched off for now:** the app opens without a login. To switch it on, set
`LOGIN_ENABLED = True` in `auth.py` and restart the app. Then everyone has to log in. The first time you open the app it asks you to create the
**superadmin** account. The superadmin sees every page and, on **Accounts and access**,
can add accounts and tick which areas each one sees (Tools, Career guide, Module 1-6),
disable or delete accounts, and reset passwords. Pages an account may not see are left out
of the app completely, so typing their URL does not open them either.

- Accounts are saved in `users.json` (not uploaded to GitHub). Passwords are stored only as
  salted PBKDF2 hashes.
- 5 wrong passwords in a row lock that username for 5 minutes.
- You are logged out after 60 minutes without activity, and when you refresh the page.
- CFP progress in the career guide is saved per account.
- Forgot the only superadmin password? Delete `users.json` and create the superadmin again
  (this removes all accounts).

## Project layout
The project is split in two:

**`interface/` – everything you see.** Edit here to change how the app looks.
- `navigation.py` – which pages exist and the sidebar menu
- `home.py` – home page with the 6 modules
- `login.py` – log in screen (only used when login is switched on)
- `admin/` – Accounts and access page, My account page
- `calculators/financial_calculator.py` – financial calculator page
- `regulation/bible.py` – Law & Regulation page
- `career/guide.py` – CFP career guide page
- `module2_investment/` – Thai mutual funds page (`dashboard.py`) and investment simulator page (`simulator.py`)

**Everything else – the logic behind the pages.** Edit here to change data or calculations.
- `app.py` – starts the app (a short launcher that calls `interface/navigation.py`)
- `auth.py` – log in checks, roles and access areas
- `career/content.py` – the CFP career guide text (summary of the TFPA documents)
- `regulation/` – the Law & Regulation entries (`topic_a.py`, `topic_b.py`, …), their sources (`sources.py`),
  the entry model (`model.py`) and
  search / self-check (`library.py`)
- `calculators/fincalc.py` – the maths of the financial calculator
- `moduleN_<topic>/` – data and calculations for each module, plus its README
- `cfp_modules.py` – names and descriptions of the 6 modules (used by the menu and home page)
- `i18n.py` / `i18n_th.py` – English/Thai switch and the Thai translations. Write on-screen text
  as `t("English text")` and add its Thai version to `i18n_th.py`
- `user_settings.py` – saves personal settings (language, CFP progress) to `user_settings.json`
- `data/` – downloaded files (not uploaded to GitHub)

## Adding a new module
1. Create a folder for its logic, e.g. `module3_insurance/` with an empty `__init__.py`.
2. Put its page file in `interface/module3_insurance/` and add an `st.Page(...)` for it under that
   module's number in `module_pages` in `interface/navigation.py`.
3. To give the module's home-page card an "Open" button, set `home_page` for that module in
   `cfp_modules.py` (and update its description).

For personal learning only. Not financial advice.
