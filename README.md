# HOBBY-PROJECT
IF 1 DAY I HAVE TO MANAGE ALL FINANCIAL THING

## CFP Toolkit
Personal practice tools, organised by the 6 modules of the Thai CFP® program.

| Module | Topic | Tools | Folder |
|---|---|---|---|
| 1 | Fundamentals of financial planning | – | – |
| 2 | Investment planning | Thai mutual fund dashboard, investment simulator (Lump sum / DCA / VCA), data downloader | [module2_investment/](module2_investment/) |
| 3 | Risk management & insurance planning | – | – |
| 4 | Retirement planning & employee benefits | – | – |
| 5 | Tax & estate planning | – | – |
| 6 | Financial plan development | – | – |

## Setup
```
pip install -r requirements.txt
```

## Run the app (only on this computer)
Double-click `run_app.bat`, or run:
```
streamlit run app.py
```
It opens at http://localhost:8501. The home page shows all 6 modules. In the sidebar each module
is a section you can open and close; the module of the page you are on opens by itself.

## Project layout
- `app.py` – starts the app and draws the sidebar menu
- `cfp_modules.py` – names and descriptions of the 6 modules (used by the menu and home page)
- `home.py` – home page with the 6 modules
- `moduleN_<topic>/` – code and README for each module
- `data/` – downloaded files (not uploaded to GitHub)

## Adding a new module
1. Create a folder, e.g. `module3_insurance/`, with an empty `__init__.py` and a page file.
2. Add an `st.Page(...)` for it under that module's number in `MODULE_PAGES` in `app.py`.
3. To give the module's home-page card an "Open" button, set `home_page` for that module in
   `cfp_modules.py` (and update its description).

For personal learning only. Not financial advice.
