"""Weekly fund snapshot for the Offline Edition (see edition.py).

build() downloads from the SEC Open API (see sec_api.py; needs the key):
- the fund catalogue (names, company, policy, official risk level RS1–RS8, dividend policy),
- the latest NAV of every fund,
- the whole NAV history of the largest funds (by fund size), plus the funds the pages pick by default
  and any symbols listed in data/snapshot_extra.txt (one per line). After the first time only the new days
  are downloaded,
and saves them in data/snapshot/ and in Documents\\CFP Toolkit\\snapshot (where the Offline Edition reads
it). The Offline Edition shows these files instead of calling the API; the normal app uses the histories as a
cache, so it only downloads the days after the snapshot.

Run `python -m module2_investment.snapshot` (the Sunday job does this; see desktop_offline/README.md).
"""

import json
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from edition import BUNDLED_SNAPSHOT, PROJECT, SNAPSHOT_DIR

TOP_FUNDS = 300                                  # largest funds that get their whole history
ALWAYS = ["ES-GQG", "K-USA-A(A)", "SCBSET"]      # picked by default on the fund pages
EXTRA_FILE = PROJECT / "data" / "snapshot_extra.txt"
OFFLINE_DATA = Path.home() / "Documents" / "CFP Toolkit" / "snapshot"  # Offline Edition's copy
NAME_COLUMNS = ["symbol", "nameEn", "nameTh", "amcCode", "amcNameEn", "policy", "dividendPolicy",
                "risk_level", "risk_code", "risk_desc", "risk_date"]


# ---------- reading (Offline Edition) ----------

def folder() -> Path | None:
    """The newest snapshot available: the weekly one, or the copy built into the app."""
    found = [d for d in (SNAPSHOT_DIR, BUNDLED_SNAPSHOT) if (d / "meta.json").exists()]
    return max(found, key=lambda d: meta(d)["as_of"]) if found else None


def meta(d: Path | None = None) -> dict:
    d = d or folder()
    return json.loads((d / "meta.json").read_text(encoding="utf-8"))


def read_catalogue() -> pd.DataFrame:
    from module2_investment import sec_api
    return sec_api.read(folder() / "funds.csv")


def read_market() -> pd.DataFrame:
    market = pd.read_csv(folder() / "market.csv.gz", parse_dates=["navDate", "dividendDate"])
    market["risk_level"] = market["risk_level"].astype("Int64")
    return market


def read_histories(names: bool = True) -> pd.DataFrame:
    hist = pd.read_csv(folder() / "history.csv.gz", parse_dates=["navDate", "dividendDate"])
    return hist.merge(read_market()[NAME_COLUMNS], on="symbol", how="left") if names else hist


# ---------- building (normal app, internet needed) ----------

def _extra_symbols() -> list[str]:
    try:
        return [s.strip() for s in EXTRA_FILE.read_text(encoding="utf-8").splitlines() if s.strip()]
    except OSError:
        return []


def build(top: int = TOP_FUNDS, workers: int = 4, log=print) -> dict:
    from module2_investment import sec_api
    from module2_investment.tables import add_growth, finish, from_nav, latest_nav

    catalogue = sec_api.refresh(log)
    as_of = sec_api.last_nav_date()
    market = latest_nav(sec_api.nav_rows(as_of - timedelta(days=10), as_of), catalogue)
    largest = market.sort_values("nav", ascending=False)["symbol"].head(top).tolist()
    wanted = list(dict.fromkeys(largest + ALWAYS + _extra_symbols()))
    symbols = [s for s in wanted if s in set(market["symbol"])]
    # Reuse the last SEC snapshot: only the days after it are downloaded.
    previous = (read_histories(names=False) if folder() and meta().get("source") == "SEC"
                else pd.DataFrame(columns=["symbol", "navDate"]))
    log(f"NAV of {len(market)} funds as of {as_of}; history of {len(symbols)} funds "
        f"({previous['symbol'].nunique()} already saved) ...")
    by_symbol = catalogue.set_index("symbol")

    def one(sym: str) -> pd.DataFrame:
        old = previous[previous["symbol"] == sym]
        start = old["navDate"].max().date() + timedelta(days=1) if len(old) else None
        rows = sec_api.nav_history_rows(by_symbol.at[sym, "proj_id"], by_symbol.at[sym, "fund_class_name"], start)
        df = finish(pd.concat([old, from_nav(rows, catalogue)], ignore_index=True)) if len(old) else from_nav(rows, catalogue)
        return add_growth(df) if not df.empty else df

    histories, failed = [], []
    with ThreadPoolExecutor(workers) as pool:
        for i, (sym, future) in enumerate([(s, pool.submit(one, s)) for s in symbols], 1):
            try:
                histories.append(future.result())
            except Exception as e:  # one fund failing should not stop the snapshot
                failed.append(sym)
                log(f"  {sym}: {e}")
            if i % 50 == 0:
                log(f"  {i}/{len(symbols)}")
    history = pd.concat(histories, ignore_index=True).drop(columns=[c for c in NAME_COLUMNS if c != "symbol"])

    tmp = SNAPSHOT_DIR.with_name("snapshot_new")
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    catalogue.to_csv(tmp / "funds.csv", index=False)
    market.to_csv(tmp / "market.csv.gz", index=False)
    history.to_csv(tmp / "history.csv.gz", index=False)
    info = {"source": "SEC", "as_of": as_of.isoformat(), "built": datetime.now().isoformat(timespec="seconds"),
            "funds": len(market), "with_history": sorted(history["symbol"].unique()), "failed": failed}
    (tmp / "meta.json").write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
    # Replace the old snapshot only once the new one is complete.
    for target in (SNAPSHOT_DIR, OFFLINE_DATA):
        shutil.rmtree(target, ignore_errors=True)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(tmp, target)
    shutil.rmtree(tmp)
    log(f"Snapshot as of {as_of}: {len(market)} funds, {len(info['with_history'])} with history, "
        f"{len(failed)} failed -> {SNAPSHOT_DIR} and {OFFLINE_DATA}")
    return info


if __name__ == "__main__":
    build(top=int(sys.argv[1]) if len(sys.argv) > 1 else TOP_FUNDS)
