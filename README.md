# HOBBY-PROJECT
IF 1 DAY I HAVE TO MANAGE ALL FINANCIAL THING

## Thai mutual fund data downloader

Downloads NAV (net asset value) data for every Thai mutual fund, the same data shown on
[thaimutualfund.com → Funds](https://www.thaimutualfund.com/AIMC/mutualFundCenter.jsp).

### How it works
The "Funds" page on thaimutualfund.com embeds an app from `weblink.settrade.com`, and that app
loads its data from a JSON API at `api.settrade.com`. Instead of scraping the web page, this
project calls that API directly:

| Endpoint | What it returns |
|---|---|
| `mutual-fund/last-business-date` | latest date with NAV data |
| `fund-nav/all?fromDate=DD/MM/YYYY&toDate=DD/MM/YYYY` | NAV of all funds (max ~1 month range) |
| `fund-nav/{SYMBOL}?fromDate=...&toDate=...` | NAV history of one fund (any range, back to launch) |
| `mutual-fund/amc/list` | asset management companies |

### Setup
```
pip install -r requirements.txt
```

### Dashboard app (runs only on this computer)
Double-click `run_app.bat`, or run:
```
streamlit run app.py
```
It opens at http://localhost:8501 with three tabs:
- **Market overview** – every fund's latest NAV, search/filter, biggest movers, CSV download
- **Fund detail** – one fund's full history since launch: factsheet-style returns
  (YTD, 3M … 10Y, since launch), growth chart, return by calendar year, drop from previous
  high, and dividend history
- **Compare funds** – up to 5 funds on one "growth of 100 THB" chart, with
  total/annualized return, volatility and max drawdown for 1M to Max
- **Fund companies** – fund size and number of funds per asset management company

### Command-line usage
```
python fetch_funds.py latest                    # all ~3,400 funds, latest NAV -> data/
python fetch_funds.py latest --excel            # also save an .xlsx
python fetch_funds.py latest --date 2026-09-30  # latest NAV as of a specific day
python fetch_funds.py history "K-USA-A(A)" --days 365
python fetch_funds.py history SCBSET --from 2026-01-01 --to 2026-06-30
python fetch_funds.py amcs                      # list of fund companies
```

CSV files are saved with UTF-8 BOM so Thai names display correctly in Excel.

### Files
- `app.py` – the dashboard (Streamlit)
- `thai_funds/client.py` – functions that call the API (reuse these in your own scripts/notebooks)
- `thai_funds/tables.py` – cleans API data into tables and calculates return/risk numbers
- `fetch_funds.py` – command-line tool that saves CSV/Excel files

### Notes
- This is an unofficial, undocumented API, so it can change without notice.
- thaimutualfund.com is run by AIMC. Its terms say the data is for information/education and
  **may not be used for commercial purposes**. Keep this project personal, and use official
  sources (e.g. the SEC Thailand Open API) for any professional or client work.
- In the dashboard, returns include dividends reinvested (total return), like official
  factsheets. The command-line `history` summary is NAV price change only.
- Renamed funds (e.g. TMB → Eastspring "ES-") keep their full history under the new symbol.
- Many funds (especially foreign-investing ones) publish NAV 1–3 days late. "Latest" therefore
  means each fund's newest NAV within the last 10 days. Check the NAV date column.
