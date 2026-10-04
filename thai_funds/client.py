"""Small client for the public API behind thaimutualfund.com's "Funds" page.

thaimutualfund.com/AIMC/mutualFundCenter.jsp embeds an app from
weblink.settrade.com, which loads its data from api.settrade.com.
This module calls the same endpoints directly so we get clean JSON
instead of scraping HTML.
"""

from datetime import date
from urllib.parse import quote

import requests

BASE_URL = "https://api.settrade.com/api/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (personal learning project)",
    "Accept": "application/json",
    "Origin": "https://weblink.settrade.com",
    "Referer": "https://weblink.settrade.com/settrade/aimc/search-nav",
}

# Earliest date to ask for when we want a fund's whole history (Thai fund data starts ~1990s).
EARLIEST_DATE = date(1990, 1, 1)


def _fmt(d: date) -> str:
    """The API expects dates as DD/MM/YYYY."""
    return d.strftime("%d/%m/%Y")


def _get(path: str, params: dict | None = None):
    resp = requests.get(BASE_URL + path, params=params, headers=HEADERS, timeout=60)
    resp.raise_for_status()
    return resp.json()


def last_business_date() -> date:
    """Latest date that has NAV data (e.g. last Friday on a weekend)."""
    value = _get("mutual-fund/last-business-date")  # "2026-10-02T00:00:00+07:00"
    return date.fromisoformat(value[:10])


def list_amcs() -> list[dict]:
    """All asset management companies (id, code, nameTh, nameEn)."""
    return _get("mutual-fund/amc/list")["fundAmcs"]


def list_investment_policies() -> list[str]:
    return _get("mutual-fund/investment-policy/list")["investmentPolicies"]


def nav_all_funds(from_date: date, to_date: date) -> list[dict]:
    """NAV of every fund between two dates. The website limits this to ~1 month."""
    params = {"fromDate": _fmt(from_date), "toDate": _fmt(to_date)}
    return _get("fund-nav/all", params)["fundNavs"]


def nav_history(symbol: str, from_date: date = EARLIEST_DATE, to_date: date | None = None) -> list[dict]:
    """NAV history of one fund. One request can cover the fund's whole life."""
    params = {"fromDate": _fmt(from_date), "toDate": _fmt(to_date or date.today())}
    return _get(f"fund-nav/{quote(symbol, safe='()')}", params)["fundNavs"]
