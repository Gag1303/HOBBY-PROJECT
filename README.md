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

## Project layout
- `app.py` – starts the app and draws the sidebar menu
- `career/` – CFP career guide (`content.py` summary text, `guide.py` page)
- `user_settings.py` – saves personal settings (language, CFP progress) to `user_settings.json`
- `cfp_modules.py` – names and descriptions of the 6 modules (used by the menu and home page)
- `i18n.py` / `i18n_th.py` – English/Thai switch and the Thai translations. Write on-screen text
  as `t("English text")` and add its Thai version to `i18n_th.py`
- `home.py` – home page with the 6 modules
- `calculators/` – financial calculator (`fincalc.py` maths, `financial_calculator.py` page)
- `moduleN_<topic>/` – code and README for each module
- `data/` – downloaded files (not uploaded to GitHub)

## Adding a new module
1. Create a folder, e.g. `module3_insurance/`, with an empty `__init__.py` and a page file.
2. Add an `st.Page(...)` for it under that module's number in `MODULE_PAGES` in `app.py`.
3. To give the module's home-page card an "Open" button, set `home_page` for that module in
   `cfp_modules.py` (and update its description).

For personal learning only. Not financial advice.
