"""Shared pieces for the Module 2 pages: cached data loaders, colors and small formatters."""

from datetime import date, timedelta

import pandas as pd
import streamlit as st

from edition import OFFLINE
from i18n import t
from module2_investment import sec_api, snapshot
from module2_investment.tables import COLUMNS, add_growth, finish, from_nav, latest_nav

# Colors (validated colorblind-safe order). Up/down use blue/red rather than color alone:
# numbers always carry a +/- sign too.
SERIES_COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
UP_COLOR, DOWN_COLOR = "#2a78d6", "#e34948"

DATA_NOTE = ("Data: SEC Open Data (the Thai SEC's Fund API). Dividend history is not published by the SEC yet, "
             "so returns of funds that pay dividends are NAV-only.")
LOOKBACK_DAYS = 10  # many funds (especially foreign ones) report NAV 1-3 days late


# ---------- data loading (cached so we don't call the API on every click) ----------
# The Offline Edition reads the weekly snapshot instead of the API (see module2_investment/snapshot.py).

@st.cache_data(ttl=3600, show_spinner=False)
def load_catalogue() -> pd.DataFrame:
    """Every active fund share class with names, company, policy, risk level and dividend policy."""
    return snapshot.read_catalogue() if OFFLINE else sec_api.read()


@st.cache_data(ttl=3600, show_spinner=False)
def load_last_date() -> date:
    if OFFLINE:
        return date.fromisoformat(snapshot.meta()["as_of"])
    return sec_api.last_nav_date()


@st.cache_data(ttl=3600, show_spinner=False)
def load_market(day: date) -> pd.DataFrame:
    """Newest NAV of every fund on or before `day`."""
    if OFFLINE:
        return snapshot.read_market()
    return latest_nav(sec_api.nav_rows(day - timedelta(days=LOOKBACK_DAYS), day), load_catalogue())


@st.cache_data(show_spinner=False)
def _snapshot_histories() -> pd.DataFrame:
    """Histories saved by the weekly snapshot (empty if there is none, or it is not from the SEC)."""
    if snapshot.folder() is None or snapshot.meta().get("source") != "SEC":
        return pd.DataFrame(columns=COLUMNS)
    return snapshot.read_histories()


@st.cache_data(ttl=3600 * 6, show_spinner=False)
def load_full_history(symbol: str, to_date: date) -> pd.DataFrame:
    """Whole NAV history of a fund with its growth. Online it starts from the weekly snapshot (if the fund is
    in it) and only downloads the days after it."""
    all_hist = _snapshot_histories()
    cached = all_hist[all_hist["symbol"] == symbol]
    if OFFLINE:
        return cached.reset_index(drop=True)
    catalogue = load_catalogue()
    row = catalogue[catalogue["symbol"] == symbol]
    if row.empty:
        return pd.DataFrame(columns=COLUMNS)
    proj_id, class_name = row["proj_id"].iat[0], row["fund_class_name"].iat[0]
    start = cached["navDate"].max().date() + timedelta(days=1) if len(cached) else None
    new = from_nav(sec_api.nav_history_rows(proj_id, class_name, start), catalogue)
    df = finish(pd.concat([cached.reindex(columns=COLUMNS), new], ignore_index=True)) if len(cached) else new
    return add_growth(df) if not df.empty else df


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
    if not OFFLINE and not sec_api.api_key():
        st.error(t("The fund pages need a free SEC Open API key. See the README (Setup → SEC Open API key)."))
        st.stop()
    if not OFFLINE and load_catalogue().empty:
        with st.spinner(t("Downloading the SEC fund list (first time only, about a minute) ...")):
            sec_api.refresh()
        load_catalogue.clear()
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
