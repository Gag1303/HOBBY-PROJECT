"""Weekly fund snapshot for the Offline Edition (see edition.py).

build() downloads, once:
- the latest NAV of every fund,
- the fund companies,
- the whole NAV history of the largest funds (by fund size), plus the funds the pages pick by default
  and any symbols listed in data/snapshot_extra.txt (one per line),
and saves them in data/snapshot/ and in Documents\\CFP Toolkit\\snapshot (where the Offline Edition reads
it). The Offline Edition shows these files instead of calling the API.

Run `python -m module2_investment.snapshot` (the Sunday job does this; see desktop_offline/README.md).
"""

import json
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd

from edition import BUNDLED_SNAPSHOT, PROJECT, SNAPSHOT_DIR

TOP_FUNDS = 300                                  # largest funds that get their whole history
ALWAYS = ["ES-GQG", "K-USA-A(A)", "SCBSET"]      # picked by default on the fund pages
EXTRA_FILE = PROJECT / "data" / "snapshot_extra.txt"
OFFLINE_DATA = Path.home() / "Documents" / "CFP Toolkit" / "snapshot"  # Offline Edition's copy
NAME_COLUMNS = ["symbol", "nameEn", "nameTh", "amcCode", "amcNameEn", "projectType"]


# ---------- reading (Offline Edition) ----------

def folder() -> Path | None:
    """The newest snapshot available: the weekly one, or the copy built into the app."""
    found = [d for d in (SNAPSHOT_DIR, BUNDLED_SNAPSHOT) if (d / "meta.json").exists()]
    return max(found, key=lambda d: meta(d)["as_of"]) if found else None


def meta(d: Path | None = None) -> dict:
    d = d or folder()
    return json.loads((d / "meta.json").read_text(encoding="utf-8"))


def read_amcs() -> pd.DataFrame:
    return pd.read_csv(folder() / "amcs.csv")


def read_market() -> pd.DataFrame:
    return pd.read_csv(folder() / "market.csv.gz", parse_dates=["navDate", "dividendDate"])


def read_histories() -> pd.DataFrame:
    hist = pd.read_csv(folder() / "history.csv.gz", parse_dates=["navDate", "dividendDate"])
    names = read_market()[NAME_COLUMNS]
    return hist.merge(names, on="symbol", how="left")


# ---------- building (normal app, internet needed) ----------

def _extra_symbols() -> list[str]:
    try:
        return [s.strip() for s in EXTRA_FILE.read_text(encoding="utf-8").splitlines() if s.strip()]
    except OSError:
        return []


def build(top: int = TOP_FUNDS, pause: float = 0.5, log=print) -> dict:
    from module2_investment import client
    from module2_investment.tables import add_growth, amc_table, latest_nav, to_dataframe

    as_of = client.last_business_date()
    amcs = amc_table()
    market = latest_nav(as_of, amcs=amcs)
    largest = market.sort_values("nav", ascending=False)["symbol"].head(top).tolist()
    wanted = list(dict.fromkeys(largest + ALWAYS + _extra_symbols()))
    symbols = [s for s in wanted if s in set(market["symbol"])]
    log(f"NAV of {len(market)} funds as of {as_of}; downloading the history of {len(symbols)} funds ...")

    histories, failed = [], []
    for i, sym in enumerate(symbols, 1):
        try:
            df = to_dataframe(client.nav_history(sym, to_date=as_of), amcs)
            if not df.empty:
                histories.append(add_growth(df.drop_duplicates(subset=["navDate"])))
        except Exception as e:  # one fund failing should not stop the snapshot
            failed.append(sym)
            log(f"  {sym}: {e}")
        if i % 50 == 0:
            log(f"  {i}/{len(symbols)}")
        time.sleep(pause)  # be gentle with the API
    history = pd.concat(histories, ignore_index=True).drop(columns=[c for c in NAME_COLUMNS if c != "symbol"])

    tmp = SNAPSHOT_DIR.with_name("snapshot_new")
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    amcs.to_csv(tmp / "amcs.csv", index=False)
    market.to_csv(tmp / "market.csv.gz", index=False)
    history.to_csv(tmp / "history.csv.gz", index=False)
    info = {"as_of": as_of.isoformat(), "built": datetime.now().isoformat(timespec="seconds"),
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
