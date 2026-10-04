"""Turn raw API rows into clean pandas tables, and compute fund statistics."""

from datetime import date, timedelta

import numpy as np
import pandas as pd

from thai_funds import client

# Columns we keep, in a readable order.
COLUMNS = [
    "navDate", "symbol", "nameEn", "nameTh", "amcCode", "amcNameEn",
    "navPerUnit", "priorNavPerUnit", "change", "changePct", "nav",
    "buyPrice", "sellPrice", "dividendValue", "dividendDate", "projectType",
]

TRADING_DAYS_PER_YEAR = 245  # approx. Thai business days in a year


def amc_table() -> pd.DataFrame:
    return pd.DataFrame(client.list_amcs()).rename(
        columns={"id": "amcId", "code": "amcCode", "nameEn": "amcNameEn", "nameTh": "amcNameTh"}
    )


def to_dataframe(rows: list[dict], amcs: pd.DataFrame | None = None) -> pd.DataFrame:
    """Turn API rows into a clean table with AMC names and % change."""
    df = pd.DataFrame(rows)
    if df.empty:
        return df

    if amcs is None:
        amcs = amc_table()
    df = df.merge(amcs[["amcId", "amcCode", "amcNameEn"]], on="amcId", how="left")
    # Some AMCs have no short code; fall back to the full name.
    df["amcCode"] = df["amcCode"].fillna(df["amcNameEn"])

    df["navDate"] = pd.to_datetime(df["navDate"].str[:10])
    df["dividendDate"] = pd.to_datetime(df["dividendDate"].str[:10])
    df["change"] = df["change"].round(4)
    df["changePct"] = (df["change"] / df["priorNavPerUnit"] * 100).round(2)
    return df[COLUMNS].sort_values(["navDate", "symbol"]).reset_index(drop=True)


def latest_nav(as_of: date, lookback_days: int = 10, amcs: pd.DataFrame | None = None) -> pd.DataFrame:
    """Newest NAV of every fund on or before `as_of`.

    Many funds (especially ones investing abroad) publish NAV 1-3 days late, so asking
    for a single day misses more than half of them. We look back a few days instead
    and keep each fund's most recent row.
    """
    rows = client.nav_all_funds(as_of - timedelta(days=lookback_days), as_of)
    df = to_dataframe(rows, amcs)
    if df.empty:
        return df
    df = df.sort_values("navDate").drop_duplicates(subset=["symbol"], keep="last")
    return df.sort_values("symbol").reset_index(drop=True)


def fund_stats(history: pd.DataFrame) -> dict:
    """Basic risk/return numbers from one fund's NAV history (price only, no dividends)."""
    nav = history.sort_values("navDate").set_index("navDate")["navPerUnit"].dropna()
    if len(nav) < 2:
        return {}
    daily = nav.pct_change().dropna()
    years = (nav.index[-1] - nav.index[0]).days / 365.25
    total = nav.iloc[-1] / nav.iloc[0] - 1
    drawdown = nav / nav.cummax() - 1
    return {
        "Start NAV": nav.iloc[0],
        "Latest NAV": nav.iloc[-1],
        "Total return %": total * 100,
        "Annualized return %": ((1 + total) ** (1 / years) - 1) * 100 if years >= 0.95 else np.nan,
        "Volatility % (yearly)": daily.std() * np.sqrt(TRADING_DAYS_PER_YEAR) * 100,
        "Max drawdown %": drawdown.min() * 100,
        "Days of data": len(nav),
    }
