"""
pull_eia.py — fetch Brent (RBRTE) and WTI (RWTC) daily spot from EIA, build the spread frame.

Usage:
    export EIA_API_KEY=...
    python scripts/pull_eia.py

Writes:
    data/raw/RBRTE.csv
    data/raw/RWTC.csv
    data/processed/spread.csv
"""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv

REPO = Path(__file__).resolve().parents[1]
RAW = REPO / "data" / "raw"
PROCESSED = REPO / "data" / "processed"
EIA_BASE = "https://api.eia.gov/v2/petroleum/pri/spt/data/"


PAGE_SIZE = 5000  # EIA hard-caps a single response at 5000 rows.


def fetch_series(series_id: str, api_key: str) -> pd.DataFrame:
    """Pull a single EIA spot series as a tidy date-indexed frame.

    EIA caps each response at 5000 rows, so we page through with `offset`
    until the API returns fewer than a full page. Daily data 2000→present is
    ~6,700 rows — without pagination only the oldest 5000 (≈2000–2019) come
    back, silently dropping the 2026 events the study is built around.
    """
    rows: list[dict] = []
    offset = 0
    while True:
        params = {
            "api_key": api_key,
            "frequency": "daily",
            "data[0]": "value",
            "facets[series][]": series_id,
            "sort[0][column]": "period",
            "sort[0][direction]": "asc",
            "offset": offset,
            "length": PAGE_SIZE,
        }
        resp = requests.get(EIA_BASE, params=params, timeout=30)
        resp.raise_for_status()
        page = resp.json()["response"]["data"]
        rows.extend(page)
        if len(page) < PAGE_SIZE:
            break
        offset += PAGE_SIZE

    if not rows:
        raise SystemExit(f"EIA returned no data for series {series_id}.")

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["period"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df[["date", "value"]].rename(columns={"value": series_id.lower()})
    df = df.dropna(subset=[series_id.lower()]).drop_duplicates("date")
    return df.sort_values("date").reset_index(drop=True)


def build_spread(brent: pd.DataFrame, wti: pd.DataFrame) -> pd.DataFrame:
    df = brent.merge(wti, on="date", how="inner").sort_values("date").reset_index(drop=True)

    # 20 Apr 2020: WTI spot settled NEGATIVE (-$36.98) during the COVID
    # demand collapse — a real, historic print, not bad data. log() is
    # undefined for non-positive prices and the cointegration analysis runs
    # on log levels, so we drop the single offending row here (the raw CSVs
    # keep it faithfully). Documented in data/README.md and flagged in the
    # paper's Limitations section.
    nonpositive = (df["rbrte"] <= 0) | (df["rwtc"] <= 0)
    if nonpositive.any():
        dropped = df.loc[nonpositive, ["date", "rbrte", "rwtc"]]
        for r in dropped.itertuples():
            print(f"  dropped non-positive price: {r.date.date()} "
                  f"brent={r.rbrte} wti={r.rwtc}")
        df = df.loc[~nonpositive].reset_index(drop=True)

    df["log_brent"] = np.log(df["rbrte"])
    df["log_wti"] = np.log(df["rwtc"])
    df["spread"] = df["rbrte"] - df["rwtc"]
    df["log_spread"] = df["log_brent"] - df["log_wti"]
    df = df.rename(columns={"rbrte": "brent", "rwtc": "wti"})
    return df[["date", "brent", "wti", "log_brent", "log_wti", "spread", "log_spread"]]


def main() -> None:
    load_dotenv()
    api_key = os.environ.get("EIA_API_KEY")
    if not api_key:
        raise SystemExit("Set EIA_API_KEY in environment or .env (register free at eia.gov/opendata).")

    RAW.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)

    brent = fetch_series("RBRTE", api_key)
    wti = fetch_series("RWTC", api_key)

    brent.to_csv(RAW / "RBRTE.csv", index=False)
    wti.to_csv(RAW / "RWTC.csv", index=False)

    spread = build_spread(brent, wti)
    spread.to_csv(PROCESSED / "spread.csv", index=False)

    print(f"Wrote {len(spread):,} rows: {spread['date'].min().date()} → {spread['date'].max().date()}")
    print(f"Latest spread: ${spread['spread'].iloc[-1]:.2f} (Brent ${spread['brent'].iloc[-1]:.2f} / WTI ${spread['wti'].iloc[-1]:.2f})")


if __name__ == "__main__":
    main()
