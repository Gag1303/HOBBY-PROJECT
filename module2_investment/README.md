# Module 2 · Investment planning – Thai mutual funds

NAV (net asset value) data, official risk level and dividend policy for every Thai mutual fund, from the
**SEC Open API** (the Thai SEC's official open data, https://secopendata.sec.or.th).

## How it works
`sec_api.py` calls the SEC Fund API (it needs a free key – see the main README, *Setup*):

| Endpoint | What it returns |
|---|---|
| `/v2/fund/general-info/profiles` | every fund and share class: names, company, policy, status |
| `/v2/fund/factsheet/risk-spectrum` | official risk level RS1–RS8 from the latest Fund Fact Sheet |
| `/v2/fund/factsheet/dividend-policy` | whether each share class has a dividend policy (Y/N) |
| `/v2/fund/daily-info/nav` | daily NAV, fund size, offer/redemption prices (all funds per day, or one class's history) |

The first three make the **fund catalogue** (`data/sec_funds.csv`, refreshed every Sunday). A fund's symbol in
the app is its share class name (e.g. `K-USA-A(A)`), or the fund's short name when it has no classes.

## Dashboard
Start the CFP Toolkit app (see the main README), then open **Module 2 · Investment planning →
Thai mutual funds** in the sidebar. It has four tabs:
- **Market overview** – every fund's latest NAV with its official risk level and policy, search/filter,
  biggest movers, CSV download
- **Fund detail** – one fund's full history since launch: risk level, factsheet-style returns
  (YTD, 3M … 10Y, since launch), NAV chart, return by calendar year, drop from previous high
- **Compare funds** – up to 5 funds on one "growth of 100 THB" chart, with
  total/annualized return, volatility and max drawdown for 1M to Max
- **Fund companies** – fund size and number of funds per asset management company

### Investment simulator (separate page: Module 2 · Investment planning → Investment simulator)
Build a portfolio (up to 8 funds). Type a total amount at the top; each fund has Weight %,
Amount (THB) and Units (at the latest NAV) that stay in step: change any one and the other
two follow. Funds you haven't set share the rest of the 100% equally (5 funds → 20% each),
and "Split equally" resets every fund to an equal share. Then back-test Lump sum,
DCA (same amount each period) or VCA (value averaging: top up to a target that grows each
period) on any date range, monthly / weekly / quarterly. Each amount invested is split by the
target weights; optional rebalancing (yearly or every period) brings drifted weights back.
Shows money-weighted return (XIRR), value and weight drift by fund, every buy/sell, the official risk level
of each fund, and a side-by-side comparison of all three strategies. The "Simulate" button on Fund detail opens
it with a portfolio of just that fund.

## Command line
Run from the project folder:
```
python -m module2_investment.sec_api     # refresh the fund catalogue (names, policy, risk level, dividend policy)
python -m module2_investment.snapshot    # weekly snapshot (runs every Sunday by itself)
```

## Files
- The two pages are in `interface/module2_investment/`: `dashboard.py` (fund dashboard) and
  `simulator.py` (investment simulator)
- `sec_api.py` – calls the SEC Open API: fund catalogue, daily NAV, one fund's history
- `common.py` – cached data loading, colors and formatting shared by both pages
- `tables.py` – turns SEC NAV rows into tables and calculates return/risk numbers
- `simulate.py` – portfolio Lump sum / DCA / VCA back-test with rebalancing, and XIRR
- `snapshot.py` – weekly snapshot: catalogue, latest NAV of all funds and the history of the ~300 largest. The
  Offline Edition reads it; the normal app uses it as a cache and only downloads the days after it.

## Notes
- **Dividends:** the SEC's dividend-history endpoint returns no data yet, so returns are **NAV-only**. For funds
  that don't pay dividends (about 80% of share classes) that is the real total return; funds that do pay show a
  warning. Add the dividend history in `sec_api.py` / `tables.py` once the SEC publishes it.
- The SEC NAV history misses a few days here and there (about 0.7% for some funds); returns are hardly affected.
- Many funds (especially foreign-investing ones) publish NAV 1–3 days late. "Latest" therefore
  means each fund's newest NAV within the last 10 days. Check the NAV date column.
- Rate limit: 5,000 calls per 5 minutes. `sec_api.get_page` waits and retries if it is reached.
