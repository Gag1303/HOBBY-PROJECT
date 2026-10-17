"""Thai mutual fund data from the SEC Open API (https://secopendata.sec.or.th) – the app's only fund source.

- catalogue(): every active fund share class with its names, fund company, investment policy, official risk
  level (RS1–RS8, from the latest Fund Fact Sheet) and dividend policy (Y/N). Saved in data/sec_funds.csv
  and refreshed weekly by the Sunday snapshot job (module2_investment/snapshot.py).
- nav_rows(): daily NAV of all funds between two dates; nav_history_rows(): one share class's NAV history.

A fund's symbol in the app is its share class name (e.g. "K-USA-A(A)"), or the fund's short name when the
fund has no classes (the SEC calls that class "main").

Dividend history: the SEC endpoint exists but returns no data yet, so returns are NAV-only for funds that pay
dividends (dividend policy "Y"). Add it here once the SEC publishes it.

Needs a free SEC Open API subscription key in .streamlit/secrets.toml (git-ignored) as SEC_API_KEY, or in the
SEC_API_KEY environment variable. Run `python -m module2_investment.sec_api` to refresh the catalogue now.
"""

import json
import os
import re
import time
import tomllib
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta

import pandas as pd

from edition import PROJECT

API_URL = "https://api.sec.or.th"
SECRETS_FILE = PROJECT / ".streamlit" / "secrets.toml"
CATALOGUE_FILE = PROJECT / "data" / "sec_funds.csv"
ACTIVE = ("Registered", "IPO")
CATALOGUE_COLUMNS = ["symbol", "proj_id", "fund_class_name", "nameEn", "nameTh", "amcCode", "amcNameEn", "policy",
                     "risk_level", "risk_code", "risk_desc", "risk_date", "dividendPolicy"]
NAV = "/v2/fund/daily-info/nav"


# ---------- calling the API ----------

def api_key() -> str:
    """The SEC Open API key, or "" when none is set up."""
    if os.environ.get("SEC_API_KEY"):
        return os.environ["SEC_API_KEY"].strip()
    try:
        return str(tomllib.loads(SECRETS_FILE.read_text(encoding="utf-8")).get("SEC_API_KEY", "")).strip()
    except (OSError, ValueError):
        return ""


def get_page(path: str, **params) -> dict:
    """One page of an endpoint ({} when the SEC has no data: HTTP 204). Waits and retries when over the rate limit."""
    key = api_key()
    if not key:
        raise RuntimeError("no SEC Open API key (set SEC_API_KEY in .streamlit/secrets.toml)")
    url = f"{API_URL}{path}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(url, headers={"Ocp-Apim-Subscription-Key": key, "Cache-Control": "no-cache"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                body = response.read()
            return json.loads(body) if body else {}
        except urllib.error.HTTPError as error:
            if error.code in (421, 429) and attempt < 4:  # over the rate limit: wait as told, then try again
                time.sleep(int(error.headers.get("Retry-After", "5")))
                continue
            raise
    return {}


def get_all(path: str, **params) -> list[dict]:
    """Every item of a paged endpoint (100 per page, following next_cursor)."""
    items, cursor = [], None
    while True:
        data = get_page(path, **params, page_size=100, **({"next_cursor": cursor} if cursor else {}))
        items += data.get("items", [])
        cursor = data.get("next_cursor")
        if not cursor:
            return items
        time.sleep(0.02)  # the SEC asks for at least 16 ms between calls


# ---------- the fund catalogue ----------

def risk_level(code) -> int | None:
    """RS1–RS8 → 1–8. The private equity codes "RS8+" and "RS81" count as 8; anything else → None."""
    match = re.fullmatch(r"RS([1-8])(\+|1)?", str(code or "").strip())
    return int(match.group(1)) if match else None


def amc_short_name(name: str) -> str:
    """'KASIKORN ASSET MANAGEMENT COMPANY LIMITED' → 'KASIKORN' (the SEC gives no short codes)."""
    short = re.sub(r"\(THAILAND\)|\bTHAILAND\b|\bASSET MANAGEMENT\b|\bFUND MANAGEMENT\b|\bINVESTMENT MANAGEMENT\b|"
                   r"\bSECURITIES\b|\bPUBLIC\b|\bCOMPANY\b|\bLIMITED\b|\bCO\.|\bLTD\.?|,", " ", str(name or "").upper())
    return re.sub(r"\s+", " ", short).strip() or str(name or "").strip()


def catalogue() -> pd.DataFrame:
    """Every active fund share class: names, company, policy, official risk level and dividend policy."""
    profiles = pd.DataFrame(get_all("/v2/fund/general-info/profiles"))
    profiles = profiles[profiles["fund_status"].isin(ACTIVE)].copy()
    profiles["symbol"] = profiles["fund_class_name"].where(profiles["fund_class_name"] != "main",
                                                           profiles["proj_abbr_name"])
    table = profiles.rename(columns={"proj_name_en": "nameEn", "proj_name_th": "nameTh", "comp_name_en": "amcNameEn",
                                     "policy_desc": "policy"})
    table["amcCode"] = table["amcNameEn"].map(amc_short_name)
    table = table.drop_duplicates("symbol")[["symbol", "proj_id", "fund_class_name", "nameEn", "nameTh", "amcCode",
                                             "amcNameEn", "policy"]]

    risk = pd.DataFrame(get_all("/v2/fund/factsheet/risk-spectrum", latest="true"))
    risk = risk.rename(columns={"risk_spectrum": "risk_code", "risk_spectrum_desc": "risk_desc", "start_date": "risk_date"})
    table = table.merge(risk[["proj_id", "risk_code", "risk_desc", "risk_date"]].drop_duplicates("proj_id"),
                        on="proj_id", how="left")
    table["risk_level"] = table["risk_code"].map(risk_level).astype("Int64")

    dividends = pd.DataFrame(get_all("/v2/fund/factsheet/dividend-policy", latest="true"))
    dividends = dividends.rename(columns={"dividend_policy": "dividendPolicy"})
    table = table.merge(dividends[["proj_id", "fund_class_name", "dividendPolicy"]]
                        .drop_duplicates(["proj_id", "fund_class_name"]), on=["proj_id", "fund_class_name"], how="left")
    return table[CATALOGUE_COLUMNS]


def refresh(log=print) -> pd.DataFrame:
    """Download the catalogue and save it to data/sec_funds.csv."""
    table = catalogue()
    CATALOGUE_FILE.parent.mkdir(exist_ok=True)
    table.to_csv(CATALOGUE_FILE, index=False, encoding="utf-8")
    log(f"SEC fund catalogue: {len(table)} share classes, {table['risk_level'].notna().sum()} with a risk level "
        f"-> {CATALOGUE_FILE} ({datetime.now():%Y-%m-%d %H:%M})")
    return table


def read(path=CATALOGUE_FILE) -> pd.DataFrame:
    """The saved catalogue (empty if it was never downloaded)."""
    try:
        table = pd.read_csv(path, dtype=str)
    except (OSError, ValueError):
        return pd.DataFrame(columns=CATALOGUE_COLUMNS)
    table["risk_level"] = pd.to_numeric(table["risk_level"], errors="coerce").astype("Int64")
    return table.reindex(columns=CATALOGUE_COLUMNS)


# ---------- daily NAV ----------

def nav_rows(start: date, end: date, workers: int = 8) -> list[dict]:
    """Daily NAV rows of all funds from start to end (one parallel download per day)."""
    days = [start + timedelta(days=i) for i in range((end - start).days + 1)]
    with ThreadPoolExecutor(workers) as pool:
        per_day = pool.map(lambda d: get_all(NAV, start_nav_date=d.isoformat(), end_nav_date=d.isoformat()), days)
    return [row for rows in per_day for row in rows]


def nav_history_rows(proj_id: str, fund_class_name: str, start: date | None = None) -> list[dict]:
    """One share class's daily NAV rows (its whole history, or from `start`)."""
    params = {"proj_id": proj_id, "fund_class_name": fund_class_name}
    if start:
        params["start_nav_date"] = start.isoformat()
    # The API matches the class name by prefix ("SCBSET" also returns SCBSETP and SCBSETE), so keep exact ones.
    return [r for r in get_all(NAV, **params) if r.get("fund_class_name") == fund_class_name]


def last_nav_date(today: date | None = None, lookback: int = 10) -> date:
    """The latest day that has NAV data (e.g. last Friday on a weekend)."""
    today = today or date.today()
    for back in range(lookback):
        day = today - timedelta(days=back)
        if get_page(NAV, start_nav_date=day.isoformat(), end_nav_date=day.isoformat(), page_size=1).get("items"):
            return day
    raise RuntimeError(f"no NAV data from the SEC in the last {lookback} days")


if __name__ == "__main__":
    refresh()
