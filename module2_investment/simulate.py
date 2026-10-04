"""Back-test investment strategies on a fund's history: Lump sum, DCA and VCA.

All strategies buy at the dividends-reinvested price (the `growth` index from tables.add_growth),
so dividends are automatically reinvested. Fees and taxes are ignored.

- Lump sum: invest the whole amount once, at the start.
- DCA (dollar cost averaging): invest the same amount every period.
- VCA (value averaging): the portfolio should grow by a fixed amount every period. Each period
  you invest whatever is needed to reach the target: more when prices fell, less when they rose.
  If the portfolio is already above target you either do nothing or (optionally) sell the excess.
"""

import numpy as np
import pandas as pd

FREQUENCIES = {"Monthly": pd.DateOffset(months=1), "Weekly": pd.DateOffset(weeks=1),
               "Quarterly": pd.DateOffset(months=3)}
STRATEGIES = ["Lump sum", "DCA", "VCA"]


def trade_dates(prices: pd.Series, start, end, frequency: str) -> pd.DatetimeIndex:
    """First NAV date on/after each scheduled date (start, start+1 period, ...) up to `end`."""
    start, end = pd.Timestamp(start), pd.Timestamp(end)
    step = FREQUENCIES[frequency]
    scheduled = []
    k = 0
    while (when := start + step * k) <= end:  # anchor every date to `start` so days don't drift
        scheduled.append(when)
        k += 1
    nav_dates = prices.index[(prices.index >= start) & (prices.index <= end)]
    pos = nav_dates.searchsorted(scheduled)
    return pd.DatetimeIndex(sorted({nav_dates[p] for p in pos if p < len(nav_dates)}))


def simulate(prices: pd.Series, start, end, strategy: str, amount: float,
             frequency: str = "Monthly", allow_sell: bool = False):
    """Run one strategy. `prices` = growth index indexed by date.

    Returns (timeline, trades, summary):
      timeline: daily value and net amount invested
      trades:   one row per buy/sell with cash, price and units
      summary:  totals, profit and money-weighted return per year
    """
    prices = prices.sort_index()
    window = prices[(prices.index >= pd.Timestamp(start)) & (prices.index <= pd.Timestamp(end))]
    if len(window) < 2:
        return pd.DataFrame(), pd.DataFrame(), {}

    if strategy == "Lump sum":
        dates = window.index[:1]
    else:
        dates = trade_dates(window, window.index[0], window.index[-1], frequency)

    units = 0.0
    trades = []
    for k, when in enumerate(dates, start=1):
        price = window[when]
        if strategy == "VCA":
            cash = amount * k - units * price  # gap between target value and current value
            if cash < 0 and not allow_sell:
                cash = 0.0
        else:
            cash = amount
        units += cash / price
        trades.append({"date": when, "price": price, "cash": cash, "units": cash / price,
                       "unitsHeld": units, "valueAfter": units * price})
    trades = pd.DataFrame(trades)

    flows = trades.set_index("date")["cash"]
    held = trades.set_index("date")["unitsHeld"].reindex(window.index).ffill().fillna(0)
    timeline = pd.DataFrame({
        "value": held * window,
        "invested": flows.reindex(window.index).fillna(0).cumsum(),  # net of any sales
    })

    money_in = flows[flows > 0].sum()
    money_out = -flows[flows < 0].sum()
    final = timeline["value"].iloc[-1]
    profit = final + money_out - money_in
    summary = {
        "Money in": money_in,
        "Money out (sold)": money_out,
        "Value now": final,
        "Profit": profit,
        "Profit %": profit / money_in * 100 if money_in else np.nan,
        "Return per year %": xirr(flows, window.index[-1], final) * 100,
        "Trades": int((flows != 0).sum()),
        "Largest single top-up": flows.max(),
    }
    return timeline, trades, summary


def xirr(flows: pd.Series, end_date: pd.Timestamp, final_value: float) -> float:
    """Money-weighted return per year (like Excel XIRR).

    `flows` are amounts invested (positive) / taken out (negative) by date. Solved by bisection.
    """
    dates = list(flows.index) + [end_date]
    cash = list(-flows.values) + [final_value]  # investor's view: paying in is negative
    years = np.array([(d - dates[0]).days / 365.25 for d in dates])
    cash = np.array(cash, dtype=float)
    if years[-1] < 1 / 365:
        return np.nan

    def npv(rate):
        return np.sum(cash / (1 + rate) ** years)

    low, high = -0.9999, 10.0
    if npv(low) * npv(high) > 0:
        return np.nan
    for _ in range(200):
        mid = (low + high) / 2
        if npv(low) * npv(mid) <= 0:
            high = mid
        else:
            low = mid
    return (low + high) / 2
