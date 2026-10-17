"""Turn SEC NAV rows into clean pandas tables, and compute fund statistics."""

import numpy as np
import pandas as pd

# Columns we keep, in a readable order. Dividend columns stay empty until the SEC publishes dividend history.
COLUMNS = [
    "navDate", "symbol", "nameEn", "nameTh", "amcCode", "amcNameEn",
    "navPerUnit", "priorNavPerUnit", "change", "changePct", "nav",
    "buyPrice", "sellPrice", "dividendValue", "dividendDate", "policy", "dividendPolicy",
    "risk_level", "risk_code", "risk_desc", "risk_date",
]
NAV_COLUMNS = {"nav_date": "navDate", "last_val": "navPerUnit", "net_asset": "nav",
               "buy_price": "buyPrice", "sell_price": "sellPrice"}

TRADING_DAYS_PER_YEAR = 245  # approx. Thai business days in a year


def finish(df: pd.DataFrame) -> pd.DataFrame:
    """Add the previous NAV and the change of each fund's rows (sorted by date, one row per day)."""
    df = df.sort_values(["symbol", "navDate"]).drop_duplicates(["symbol", "navDate"], keep="last")
    df["priorNavPerUnit"] = df.groupby("symbol")["navPerUnit"].shift()
    df["change"] = (df["navPerUnit"] - df["priorNavPerUnit"]).round(4)
    df["changePct"] = (df["change"] / df["priorNavPerUnit"] * 100).round(2)
    return df.reindex(columns=COLUMNS).sort_values(["navDate", "symbol"]).reset_index(drop=True)


def from_nav(rows: list[dict], catalogue: pd.DataFrame) -> pd.DataFrame:
    """SEC daily NAV rows → a clean table with fund names, company, policy, risk level and % change."""
    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame(columns=COLUMNS)
    df = df.rename(columns=NAV_COLUMNS)
    df["navDate"] = pd.to_datetime(df["navDate"])
    for col in ("buyPrice", "sellPrice"):  # ETFs trade on the exchange and report 0
        df[col] = df[col].where(df[col] > 0)
    df["dividendValue"], df["dividendDate"] = np.nan, pd.NaT
    df = df.merge(catalogue, on=["proj_id", "fund_class_name"], how="inner")  # only funds we know
    return finish(df)


def latest_nav(rows: list[dict], catalogue: pd.DataFrame) -> pd.DataFrame:
    """Newest NAV of every fund in the rows (many funds, especially foreign ones, report 1-3 days late,
    so the rows should cover the last ~10 days)."""
    df = from_nav(rows, catalogue)
    if df.empty:
        return df
    df = df.sort_values("navDate").drop_duplicates(subset=["symbol"], keep="last")
    return df.sort_values("symbol").reset_index(drop=True)


def add_growth(history: pd.DataFrame) -> pd.DataFrame:
    """Add a `growth` column: value of 1 THB invested at the start, dividends reinvested (when known).

    On the day a fund goes ex-dividend its NAV drops by the dividend, so that day's return
    is (NAV + dividend) / previous NAV - 1. This is the "total return" used in factsheets.
    """
    df = history.sort_values("navDate").reset_index(drop=True).copy()
    dividend = pd.to_numeric(df["dividendValue"], errors="coerce").fillna(0)
    daily = (df["navPerUnit"] + dividend) / df["navPerUnit"].shift() - 1
    df["growth"] = (1 + daily.fillna(0)).cumprod()
    return df


def _growth_series(history: pd.DataFrame) -> pd.Series:
    if "growth" not in history:
        history = add_growth(history)
    s = history.sort_values("navDate").set_index("navDate")["growth"].dropna()
    return s / s.iloc[0] if len(s) else s


def _annualize(total: float, years: float) -> float:
    return (1 + total) ** (1 / years) - 1


def fund_stats(history: pd.DataFrame) -> dict:
    """Risk/return numbers for one fund over the rows given (dividends reinvested)."""
    growth = _growth_series(history)
    nav = history.sort_values("navDate")["navPerUnit"]
    if len(growth) < 2:
        return {}
    daily = growth.pct_change().dropna()
    years = (growth.index[-1] - growth.index[0]).days / 365.25
    total = growth.iloc[-1] - 1
    return {
        "Start NAV": nav.iloc[0],
        "Latest NAV": nav.iloc[-1],
        "Total return %": total * 100,
        "Annualized return %": _annualize(total, years) * 100 if years >= 0.95 else np.nan,
        "Volatility % (yearly)": daily.std() * np.sqrt(TRADING_DAYS_PER_YEAR) * 100,
        "Max drawdown %": drawdown(history).min() * 100,
        "Days of data": len(growth),
    }


def drawdown(history: pd.DataFrame) -> pd.Series:
    """How far below its previous peak the fund is on each day (0 = at a new high)."""
    growth = _growth_series(history)
    return growth / growth.cummax() - 1


# Factsheet-style periods: (label, months back). None = since launch, 0 = year to date.
PERFORMANCE_PERIODS = [
    ("YTD", 0), ("3M", 3), ("6M", 6), ("1Y", 12), ("3Y", 36), ("5Y", 60), ("10Y", 120),
    ("Since launch", None),
]


def period_returns(history: pd.DataFrame) -> pd.DataFrame:
    """Returns for standard periods up to the latest date, like a fund factsheet.

    Periods of 1 year or more are annualized (% per year), as factsheets show them.
    """
    growth = _growth_series(history)
    end = growth.index[-1]
    rows = []
    for label, months in PERFORMANCE_PERIODS:
        if months is None:
            start = growth.index[0]
        elif months == 0:
            start = pd.Timestamp(end.year - 1, 12, 31)
        else:
            start = end - pd.DateOffset(months=months)

        if start < growth.index[0] and months is not None:
            ret, annual = np.nan, np.nan  # fund is younger than this period
        else:
            start_value = growth[growth.index <= start].iloc[-1] if months is not None else growth.iloc[0]
            ret = growth.iloc[-1] / start_value - 1
            years = (end - max(start, growth.index[0])).days / 365.25
            annual = _annualize(ret, years) if years >= 0.95 else np.nan
        rows.append({"Period": label, "Return %": ret * 100, "Per year %": annual * 100})
    return pd.DataFrame(rows)


def calendar_year_returns(history: pd.DataFrame) -> pd.DataFrame:
    """Return for each calendar year (dividends reinvested). First/current years are partial."""
    growth = _growth_series(history)
    year_end = growth.groupby(growth.index.year).last()
    previous = year_end.shift()
    previous.iloc[0] = growth.iloc[0]  # first year: measured from launch
    out = pd.DataFrame({"Year": year_end.index, "Return %": (year_end / previous - 1).values * 100})
    out["Note"] = ""
    if growth.index[0].month > 1 or growth.index[0].day > 10:
        out.loc[out.index[0], "Note"] = f"from launch ({growth.index[0]:%d %b})"
    if growth.index[-1].month < 12 or growth.index[-1].day < 20:
        out.loc[out.index[-1], "Note"] = f"year to date ({growth.index[-1]:%d %b})"
    return out


def dividends(history: pd.DataFrame) -> pd.DataFrame:
    """Dividends paid per unit, newest first."""
    d = history[history["dividendValue"].notna() & (history["dividendValue"] > 0)]
    d = d.assign(yieldPct=d["dividendValue"] / d["priorNavPerUnit"] * 100)
    return d[["navDate", "dividendDate", "dividendValue", "yieldPct"]].sort_values("navDate", ascending=False)
