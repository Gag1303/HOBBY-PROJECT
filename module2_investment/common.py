"""Shared pieces for the Module 2 pages: cached data loaders, colors and small formatters."""

from datetime import date

import pandas as pd
import streamlit as st

from edition import OFFLINE
from i18n import t
from module2_investment import client, snapshot
from module2_investment.tables import add_growth, amc_table, latest_nav, to_dataframe

# Colors (validated colorblind-safe order). Up/down use blue/red rather than color alone:
# numbers always carry a +/- sign too.
SERIES_COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
UP_COLOR, DOWN_COLOR = "#2a78d6", "#e34948"

DATA_NOTE = ("Data: thaimutualfund.com (AIMC) via api.settrade.com. "
             "For personal/educational use only, not for commercial use.")


# ---------- data loading (cached so we don't call the API on every click) ----------
# The Offline Edition reads the weekly snapshot instead of the API (see module2_investment/snapshot.py).

@st.cache_data(ttl=3600, show_spinner=False)
def load_last_date() -> date:
    if OFFLINE:
        return date.fromisoformat(snapshot.meta()["as_of"])
    return client.last_business_date()


@st.cache_data(ttl=3600 * 24, show_spinner=False)
def load_amcs() -> pd.DataFrame:
    return snapshot.read_amcs() if OFFLINE else amc_table()


@st.cache_data(ttl=3600, show_spinner=False)
def load_market(day: date) -> pd.DataFrame:
    return snapshot.read_market() if OFFLINE else latest_nav(day, amcs=load_amcs())


@st.cache_data(show_spinner=False)
def _snapshot_histories() -> pd.DataFrame:
    return snapshot.read_histories()


@st.cache_data(ttl=3600 * 6, show_spinner=False)
def load_full_history(symbol: str, to_date: date) -> pd.DataFrame:
    """Whole NAV history of a fund (one fast request), with the dividends-reinvested growth."""
    if OFFLINE:
        all_hist = _snapshot_histories()
        return all_hist[all_hist["symbol"] == symbol].reset_index(drop=True)
    df = to_dataframe(client.nav_history(symbol, to_date=to_date), load_amcs())
    return add_growth(df.drop_duplicates(subset=["navDate"])) if not df.empty else df


def history_symbols() -> set[str] | None:
    """Funds whose history can be shown: those in the snapshot offline, None (= all) online."""
    return set(snapshot.meta()["with_history"]) if OFFLINE else None


def snapshot_caption() -> None:
    """Offline Edition: say which snapshot the fund pages show."""
    if OFFLINE:
        info = snapshot.meta()
        st.info("📦 " + t("Offline Edition: fund data from the weekly snapshot as of {day}. Full history is "
                          "available for the {n} largest funds.", day=f"{date.fromisoformat(info['as_of']):%d %b %Y}",
                          n=len(info["with_history"])))


def last_date_or_stop() -> date:
    """Latest NAV date, or show an error and stop the page if the API (or offline snapshot) can't be read."""
    if OFFLINE and snapshot.folder() is None:
        st.error(t("No fund snapshot found. Run the weekly snapshot on the computer with the normal app."))
        st.stop()
    try:
        return load_last_date()
    except Exception as e:  # network down, API changed, ...
        st.error(t("Could not reach the data source: {error}", error=e))
        st.stop()


# ---------- formatting ----------

LABEL_SEP = "  ·  "


def fund_label(symbol: str, name: str | None) -> str:
    """'SYMBOL  ·  Fund name' as shown in fund pickers. symbol_of() reverses it."""
    return f"{symbol}{LABEL_SEP}{name or ''}"


def symbol_of(label: str) -> str:
    return label.split(LABEL_SEP)[0]


def csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")  # BOM so Excel shows Thai text


def signed(x: float, digits: int = 2) -> str:
    return "–" if pd.isna(x) else f"{x:+.{digits}f}%"
