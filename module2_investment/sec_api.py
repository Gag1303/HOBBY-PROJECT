"""Official fund data from the SEC Open API (https://secopendata.sec.or.th): each fund's risk level.

The SEC reports a fund's risk level (risk spectrum RS1–RS8) per fund project, from the latest Fund Fact
Sheet. The app's fund list (from Settrade) is per share class, e.g. "K-USA-A(A)", so risk_table() maps
each class to its fund project through the SEC fund profiles.

Needs a free SEC Open API subscription key in .streamlit/secrets.toml (git-ignored) as SEC_API_KEY, or in
the SEC_API_KEY environment variable. The table is saved in data/sec_risk.csv and refreshed weekly by the
Sunday snapshot job (module2_investment/snapshot.py).

Run `python -m module2_investment.sec_api` to download it now.
"""

import json
import os
import re
import time
import tomllib
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

import pandas as pd

from edition import PROJECT

API_URL = "https://api.sec.or.th"
SECRETS_FILE = PROJECT / ".streamlit" / "secrets.toml"
RISK_FILE = PROJECT / "data" / "sec_risk.csv"
ACTIVE = ("Registered", "IPO")
COLUMNS = ["symbol", "proj_id", "risk_level", "risk_code", "risk_desc", "risk_date"]


def api_key() -> str:
    """The SEC Open API key, or "" when none is set up."""
    if os.environ.get("SEC_API_KEY"):
        return os.environ["SEC_API_KEY"].strip()
    try:
        return str(tomllib.loads(SECRETS_FILE.read_text(encoding="utf-8")).get("SEC_API_KEY", "")).strip()
    except (OSError, ValueError):
        return ""


def get_all(path: str, **params) -> list[dict]:
    """Every item of a paged SEC Open API endpoint (100 per page, following next_cursor)."""
    key = api_key()
    if not key:
        raise RuntimeError("no SEC Open API key (set SEC_API_KEY in .streamlit/secrets.toml)")
    items, cursor = [], None
    while True:
        query = dict(params, page_size=100, **({"next_cursor": cursor} if cursor else {}))
        request = urllib.request.Request(f"{API_URL}{path}?{urllib.parse.urlencode(query)}",
                                         headers={"Ocp-Apim-Subscription-Key": key, "Cache-Control": "no-cache"})
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                data = json.load(response)
        except urllib.error.HTTPError as error:
            if error.code in (421, 429):  # over the rate limit: wait as told, then try again
                time.sleep(int(error.headers.get("Retry-After", "5")))
                continue
            raise
        items += data.get("items", [])
        cursor = data.get("next_cursor")
        if not cursor:
            return items
        time.sleep(0.05)  # the SEC asks for at least 16 ms between calls


def risk_level(code) -> int | None:
    """RS1–RS8 → 1–8. The private equity codes "RS8+" and "RS81" count as 8; anything else → None."""
    match = re.fullmatch(r"RS([1-8])(\+|1)?", str(code or "").strip())
    return int(match.group(1)) if match else None


def risk_table() -> pd.DataFrame:
    """Official risk level of every active fund, one row per app fund symbol (share class)."""
    profiles = pd.DataFrame(get_all("/v2/fund/general-info/profiles"))
    profiles = profiles[profiles["fund_status"].isin(ACTIVE)]
    # A class fund's symbol is its class name; a fund without classes ("main") uses the fund's short name.
    profiles["symbol"] = profiles["fund_class_name"].where(profiles["fund_class_name"] != "main",
                                                           profiles["proj_abbr_name"])
    risk = pd.DataFrame(get_all("/v2/fund/factsheet/risk-spectrum", latest="true"))
    risk = risk.rename(columns={"risk_spectrum": "risk_code", "risk_spectrum_desc": "risk_desc",
                                "start_date": "risk_date"})
    table = profiles[["symbol", "proj_id"]].drop_duplicates("symbol").merge(
        risk[["proj_id", "risk_code", "risk_desc", "risk_date"]].drop_duplicates("proj_id"), on="proj_id", how="left")
    table["risk_level"] = table["risk_code"].map(risk_level).astype("Int64")
    return table[COLUMNS]


def refresh(log=print) -> pd.DataFrame:
    """Download the risk table and save it to data/sec_risk.csv."""
    table = risk_table()
    RISK_FILE.parent.mkdir(exist_ok=True)
    table.to_csv(RISK_FILE, index=False, encoding="utf-8")
    log(f"SEC risk levels: {table['risk_level'].notna().sum()} of {len(table)} fund classes "
        f"-> {RISK_FILE} ({datetime.now():%Y-%m-%d %H:%M})")
    return table


def read(path=RISK_FILE) -> pd.DataFrame:
    """The saved risk table (empty if it was never downloaded)."""
    try:
        table = pd.read_csv(path, dtype={"risk_code": str, "risk_desc": str, "risk_date": str})
    except (OSError, ValueError):
        return pd.DataFrame(columns=COLUMNS)
    table["risk_level"] = table["risk_level"].astype("Int64")
    return table


if __name__ == "__main__":
    refresh()
