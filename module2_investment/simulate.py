"""Back-test investment strategies on a portfolio of funds: Lump sum, DCA and VCA.

A portfolio is a list of funds with target weights (a single fund is just weight 100%).
All strategies buy at the dividends-reinvested price (the `growth` index from tables.add_growth),
so dividends are automatically reinvested. Fees and taxes are ignored.

- Lump sum: invest the whole amount once, at the start.
- DCA (dollar cost averaging): invest the same amount every period.
- VCA (value averaging): the portfolio should grow by a fixed amount every period. Each period
  you invest whatever is needed to reach the target: more when prices fell, less when they rose.
  If the portfolio is already above target you either do nothing or (optionally) sell the excess.

Every amount invested is split across the funds by their target weights. Over time the funds
drift away from those weights; rebalancing (yearly or every period) moves them back.
"""

import numpy as np
import pandas as pd

FREQUENCIES = {"Monthly": pd.DateOffset(months=1), "Weekly": pd.DateOffset(weeks=1),
               "Quarterly": pd.DateOffset(months=3)}
STRATEGIES = ["Lump sum", "DCA", "VCA"]
REBALANCING = ["None", "Yearly", "Every period"]


def align_prices(series: dict[str, pd.Series]) -> pd.DataFrame:
    """Put several funds' price series on one date index (one column per fund).

    Funds publish NAV on slightly different days (e.g. foreign funds skip Thai holidays
    differently), so a missing day keeps the fund's last NAV. Rows start on the first date
    on which every fund has a price.
    """
    return pd.DataFrame(series).sort_index().ffill().dropna()


def _scheduled(index: pd.DatetimeIndex, start, end, step: pd.DateOffset) -> pd.DatetimeIndex:
    """First date in `index` on/after each of start, start+step, start+2*step, ... up to `end`."""
    start, end = pd.Timestamp(start), pd.Timestamp(end)
    scheduled = []
    k = 0
    while (when := start + step * k) <= end:  # anchor every date to `start` so days don't drift
        scheduled.append(when)
        k += 1
    dates = index[(index >= start) & (index <= end)]
    pos = dates.searchsorted(scheduled)
    return pd.DatetimeIndex(sorted({dates[p] for p in pos if p < len(dates)}))


def trade_dates(prices: pd.Series | pd.DataFrame, start, end, frequency: str) -> pd.DatetimeIndex:
    return _scheduled(prices.index, start, end, FREQUENCIES[frequency])


def simulate(prices: pd.Series | pd.DataFrame, start, end, strategy: str, amount: float,
             frequency: str = "Monthly", allow_sell: bool = False,
             weights: dict[str, float] | None = None, rebalance: str = "None"):
    """Run one strategy on one fund (Series) or a portfolio (DataFrame, one column per fund).

    `weights` maps column -> target weight (any scale; normalized to 100%). Default: equal.
    Returns (timeline, trades, summary, by_fund):
      timeline: daily total value and net amount invested
      trades:   one row per buy/sell with cash and portfolio value after
      summary:  totals, profit and money-weighted return per year
      by_fund:  daily value held in each fund
    """
    if isinstance(prices, pd.Series):
        prices = prices.to_frame(prices.name or "fund")
    prices = prices.sort_index()
    window = prices[(prices.index >= pd.Timestamp(start)) & (prices.index <= pd.Timestamp(end))]
    if len(window) < 2:
        return pd.DataFrame(), pd.DataFrame(), {}, pd.DataFrame()

    w = pd.Series(weights if weights else 1.0, index=window.columns, dtype=float).fillna(0)
    w = (w / w.sum()).values

    # Schedules count from the requested start date (e.g. the 2nd of each month), even if the
    # first NAV comes a few days later because the start was a weekend or holiday.
    first, last = pd.Timestamp(start), window.index[-1]
    buys = window.index[:1] if strategy == "Lump sum" else trade_dates(window, first, last, frequency)
    if rebalance == "Yearly":
        rebalances = _scheduled(window.index, first, last, pd.DateOffset(years=1))[1:]
    elif rebalance == "Every period":
        rebalances = trade_dates(window, first, last, frequency)[1:]
    else:
        rebalances = pd.DatetimeIndex([])
    buy_set, rebalance_set = set(buys), set(rebalances)

    units = np.zeros(len(window.columns))
    holdings, trades = {}, []
    k = 0
    for when in sorted(buy_set | rebalance_set):
        price = window.loc[when].values
        value = units @ price
        if when in rebalance_set and value > 0:
            units = value * w / price  # back to target weights; total value unchanged
        if when in buy_set:
            k += 1
            if strategy == "VCA":
                cash = amount * k - value  # gap between target value and current value
                if cash < 0 and not allow_sell:
                    cash = 0.0
            else:
                cash = amount
            if cash >= 0:
                units = units + cash * w / price
            else:
                units = units * (1 + cash / value)  # sell the same share of every fund
            trades.append({"date": when, "cash": cash, "valueAfter": units @ price})
        holdings[when] = units.copy()
    trades = pd.DataFrame(trades)

    held = (pd.DataFrame(holdings, index=window.columns).T
            .reindex(window.index).ffill().fillna(0))
    by_fund = held * window
    flows = trades.set_index("date")["cash"]
    timeline = pd.DataFrame({
        "value": by_fund.sum(axis=1),
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
        "Return per year %": xirr(flows, last, final) * 100,
        "Trades": int((flows != 0).sum()),
        "Largest single top-up": flows.max(),
    }
    return timeline, trades, summary, by_fund


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
