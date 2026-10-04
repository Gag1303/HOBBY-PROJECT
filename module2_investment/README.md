# Module 2 · Investment planning – Thai mutual funds

NAV (net asset value) data for every Thai mutual fund, the same data shown on
[thaimutualfund.com → Funds](https://www.thaimutualfund.com/AIMC/mutualFundCenter.jsp).

## How it works
The "Funds" page on thaimutualfund.com embeds an app from `weblink.settrade.com`, and that app
loads its data from a JSON API at `api.settrade.com`. Instead of scraping the web page, this
project calls that API directly:

| Endpoint | What it returns |
|---|---|
| `mutual-fund/last-business-date` | latest date with NAV data |
| `fund-nav/all?fromDate=DD/MM/YYYY&toDate=DD/MM/YYYY` | NAV of all funds (max ~1 month range) |
| `fund-nav/{SYMBOL}?fromDate=...&toDate=...` | NAV history of one fund (any range, back to launch) |
| `mutual-fund/amc/list` | asset management companies |

## Dashboard
Start the CFP Toolkit app (see the main README), then open **Module 2 · Investment planning →
Thai mutual funds** in the sidebar. It has four tabs:
- **Market overview** – every fund's latest NAV, search/filter, biggest movers, CSV download
- **Fund detail** – one fund's full history since launch: factsheet-style returns
  (YTD, 3M … 10Y, since launch), NAV chart, return by calendar year, drop from previous
  high, and dividend history
- **Compare funds** – up to 5 funds on one "growth of 100 THB" chart, with
  total/annualized return, volatility and max drawdown for 1M to Max
- **Fund companies** – fund size and number of funds per asset management company

### Investment simulator (separate page: Module 2 · Investment planning → Investment simulator)
Build a portfolio (a list of up to 8 funds with target weights), then back-test Lump sum,
DCA (same amount each period) or VCA (value averaging: top up to a target that grows each
period) on any date range, monthly / weekly / quarterly. Each amount invested is split by the
target weights; optional rebalancing (yearly or every period) brings drifted weights back.
Shows money-weighted return (XIRR), value and weight drift by fund, every buy/sell, and a
side-by-side comparison of all three strategies. The "Simulate" button on Fund detail opens it
with a portfolio of just that fund.

## Command-line usage
Run from the project folder:
```
python -m module2_investment.fetch_funds latest                    # all ~3,400 funds, latest NAV -> data/
python -m module2_investment.fetch_funds latest --excel            # also save an .xlsx
python -m module2_investment.fetch_funds latest --date 2026-09-30  # latest NAV as of a specific day
python -m module2_investment.fetch_funds history "K-USA-A(A)" --days 365
python -m module2_investment.fetch_funds history SCBSET --from 2026-01-01 --to 2026-06-30
python -m module2_investment.fetch_funds amcs                      # list of fund companies
```

CSV files are saved with UTF-8 BOM so Thai names display correctly in Excel.

## Files
- `dashboard.py` – the fund dashboard page (Streamlit)
- `simulator.py` – the investment simulator page
- `common.py` – cached data loading, colors and formatting shared by both pages
- `client.py` – functions that call the API (reuse these in your own scripts/notebooks)
- `tables.py` – cleans API data into tables and calculates return/risk numbers
- `simulate.py` – portfolio Lump sum / DCA / VCA back-test with rebalancing, and XIRR
- `fetch_funds.py` – command-line tool that saves CSV/Excel files

## Notes
- This is an unofficial, undocumented API, so it can change without notice.
- thaimutualfund.com is run by AIMC. Its terms say the data is for information/education and
  **may not be used for commercial purposes**. Keep this project personal, and use official
  sources (e.g. the SEC Thailand Open API) for any professional or client work.
- In the dashboard, returns include dividends reinvested (total return), like official
  factsheets. The command-line `history` summary is NAV price change only.
- Renamed funds (e.g. TMB → Eastspring "ES-") keep their full history under the new symbol.
- Many funds (especially foreign-investing ones) publish NAV 1–3 days late. "Latest" therefore
  means each fund's newest NAV within the last 10 days. Check the NAV date column.
