"""Shared pieces for the Module 2 pages: cached data loaders, colors and small formatters."""

from datetime import date

import pandas as pd
import streamlit as st

from module2_investment import client
from module2_investment.tables import add_growth, amc_table, latest_nav, to_dataframe

# Colors (validated colorblind-safe order). Up/down use blue/red rather than color alone:
# numbers always carry a +/- sign too.
SERIES_COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
UP_COLOR, DOWN_COLOR = "#2a78d6", "#e34948"

DATA_NOTE = ("Data: thaimutualfund.com (AIMC) via api.settrade.com. "
             "For personal/educational use only, not for commercial use.")


# ---------- data loading (cached so we don't call the API on every click) ----------

@st.cache_data(ttl=3600, show_spinner=False)
def load_last_date() -> date:
    return client.last_business_date()


@st.cache_data(ttl=3600 * 24, show_spinner=False)
def load_amcs() -> pd.DataFrame:
    return amc_table()


@st.cache_data(ttl=3600, show_spinner=False)
def load_market(day: date) -> pd.DataFrame:
    return latest_nav(day, amcs=load_amcs())


@st.cache_data(ttl=3600 * 6, show_spinner=False)
def load_full_history(symbol: str, to_date: date) -> pd.DataFrame:
    """Whole NAV history of a fund (one fast request), with the dividends-reinvested growth."""
    df = to_dataframe(client.nav_history(symbol, to_date=to_date), load_amcs())
    return add_growth(df.drop_duplicates(subset=["navDate"])) if not df.empty else df


def last_date_or_stop() -> date:
    """Latest NAV date, or show an error and stop the page if the API can't be reached."""
    try:
        return load_last_date()
    except Exception as e:  # network down, API changed, ...
        st.error(f"Could not reach the data source: {e}")
        st.stop()


# ---------- formatting ----------

def csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")  # BOM so Excel shows Thai text


def signed(x: float, digits: int = 2) -> str:
    return "–" if pd.isna(x) else f"{x:+.{digits}f}%"
