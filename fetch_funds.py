"""Download Thai mutual fund NAV data to CSV / Excel.

Examples:
    python fetch_funds.py latest                      # all funds, latest NAV
    python fetch_funds.py latest --excel              # same, also save .xlsx
    python fetch_funds.py history K-USA-A(A) --days 365
    python fetch_funds.py history SCBSET --from 2026-01-01 --to 2026-06-30
    python fetch_funds.py amcs                        # list of fund companies

Files are saved in the data/ folder.
"""

import argparse
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

from thai_funds import client

DATA_DIR = Path(__file__).parent / "data"

# Columns we keep, in a readable order.
COLUMNS = [
    "navDate", "symbol", "nameEn", "nameTh", "amcCode", "amcNameEn",
    "navPerUnit", "priorNavPerUnit", "change", "changePct", "nav",
    "buyPrice", "sellPrice", "dividendValue", "dividendDate", "projectType",
]


def to_dataframe(rows: list[dict]) -> pd.DataFrame:
    """Turn API rows into a clean table with AMC names and % change."""
    df = pd.DataFrame(rows)
    if df.empty:
        return df

    amcs = pd.DataFrame(client.list_amcs()).rename(
        columns={"id": "amcId", "code": "amcCode", "nameEn": "amcNameEn", "nameTh": "amcNameTh"}
    )
    df = df.merge(amcs[["amcId", "amcCode", "amcNameEn"]], on="amcId", how="left")

    df["navDate"] = pd.to_datetime(df["navDate"].str[:10])
    df["dividendDate"] = pd.to_datetime(df["dividendDate"].str[:10])
    df["change"] = df["change"].round(4)
    df["changePct"] = (df["change"] / df["priorNavPerUnit"] * 100).round(2)
    return df[COLUMNS].sort_values(["navDate", "symbol"]).reset_index(drop=True)


def save(df: pd.DataFrame, name: str, excel: bool) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    csv_path = DATA_DIR / f"{name}.csv"
    # utf-8-sig so Excel shows Thai text correctly when opening the CSV.
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"Saved {len(df)} rows -> {csv_path}")
    if excel:
        xlsx_path = DATA_DIR / f"{name}.xlsx"
        df.to_excel(xlsx_path, index=False)
        print(f"Saved {len(df)} rows -> {xlsx_path}")


def cmd_latest(args):
    day = args.date or client.last_business_date()
    print(f"Fetching NAV of all funds on {day} ...")
    df = to_dataframe(client.nav_all_funds(day, day))
    save(df, f"nav_all_{day}", args.excel)

    if not df.empty:
        top = df.dropna(subset=["changePct"]).sort_values("changePct", ascending=False)
        cols = ["symbol", "navPerUnit", "changePct"]
        print("\nTop 5 gainers today:\n", top.head(5)[cols].to_string(index=False))
        print("\nTop 5 losers today:\n", top.tail(5)[cols].to_string(index=False))


def cmd_history(args):
    to_date = args.to or client.last_business_date()
    from_date = args.from_ or to_date - timedelta(days=args.days)
    print(f"Fetching {args.symbol} from {from_date} to {to_date} ...")
    df = to_dataframe(client.nav_history(args.symbol, from_date, to_date))
    if df.empty:
        print("No data found. Check the fund symbol (e.g. K-USA-A(A), SCBSET).")
        return
    df = df.drop_duplicates(subset=["navDate"])
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in args.symbol)
    save(df, f"history_{safe_name}_{from_date}_{to_date}", args.excel)

    first, last = df.iloc[0], df.iloc[-1]
    ret = (last["navPerUnit"] / first["navPerUnit"] - 1) * 100
    print(f"\nNAV {first['navPerUnit']} ({first['navDate']:%Y-%m-%d}) -> "
          f"{last['navPerUnit']} ({last['navDate']:%Y-%m-%d}) = {ret:+.2f}% "
          "(price change only, dividends not included)")


def cmd_amcs(args):
    df = pd.DataFrame(client.list_amcs())
    save(df, "amcs", args.excel)


def main():
    parser = argparse.ArgumentParser(description="Download Thai mutual fund NAV data.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("latest", help="NAV of all funds for one day")
    p.add_argument("--date", type=date.fromisoformat, help="YYYY-MM-DD (default: latest)")
    p.set_defaults(func=cmd_latest)

    p = sub.add_parser("history", help="NAV history of one fund")
    p.add_argument("symbol", help="fund symbol, e.g. K-USA-A(A)")
    p.add_argument("--from", dest="from_", type=date.fromisoformat, help="YYYY-MM-DD")
    p.add_argument("--to", type=date.fromisoformat, help="YYYY-MM-DD (default: latest)")
    p.add_argument("--days", type=int, default=365, help="days back if --from not given")
    p.set_defaults(func=cmd_history)

    p = sub.add_parser("amcs", help="list of asset management companies")
    p.set_defaults(func=cmd_amcs)

    for p in sub.choices.values():
        p.add_argument("--excel", action="store_true", help="also save an .xlsx file")

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
