"""Fetch missing data series needed by the 50-strategy validation.

Reuses the existing parquet cache layout (`finance-data-api/data/...`).
- FRED series → `macro/<series_id>.parquet` (single-column 'value')
- New ETFs (VEU EFA IEF VNQ DBC BIL BND AGG SHY USMV QUAL MTUM VLUE SPLV
  VBR IJS GLDM, and 11 SPDR sector ETFs) → `prices/<symbol>.parquet`

Run:
    python validation50/data_acq.py            # full sync
    python validation50/data_acq.py --only fred,etfs
"""
from __future__ import annotations

import argparse
import io
import pathlib
import sys
import time
import urllib.request

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "finance-data-api"))

from storage import Storage  # noqa: E402
from fetchers import fetch_yf  # noqa: E402


# ---------------------------------------------------------------------------
# FRED series — public CSV, no API key required
# ---------------------------------------------------------------------------
FRED_SERIES = [
    "T10Y3M",         # 10Y minus 3M Treasury spread (pp)
    "T10Y2Y",         # 10Y minus 2Y Treasury spread (pp)
    "BAMLH0A0HYM2",   # ICE BofA US High Yield OAS
    "NFCI",           # Chicago Fed National Financial Conditions Index (weekly)
    "CFNAI",          # Chicago Fed National Activity Index (monthly)
    "DGS3MO",         # 3-month Treasury constant maturity (%)
    "DGS10",          # 10Y Treasury constant maturity (%)
    "DGS2",           # 2Y Treasury constant maturity (%)
    "DTWEXBGS",       # USD Broad index daily
    "DEXCHUS",        # CNY/USD exchange rate
    "GDPC1",          # Real GDP (quarterly, used as macro context)
    "UNRATE",         # Unemployment rate (monthly)
    "CPILFESL",       # Core CPI
]


def fetch_fred(series_id: str, retries: int = 3, start: str = "1990-01-01") -> pd.Series:
    url = (f"https://fred.stlouisfed.org/graph/fredgraph.csv"
           f"?id={series_id}&cosd={start}")
    for i in range(retries):
        try:
            data = urllib.request.urlopen(url, timeout=15).read().decode()
            df = pd.read_csv(io.StringIO(data))
            date_col = df.columns[0]
            val_col = df.columns[1]
            df[val_col] = pd.to_numeric(df[val_col], errors="coerce")
            df[date_col] = pd.to_datetime(df[date_col])
            df = df.dropna(subset=[val_col])
            return df.set_index(date_col)[val_col].rename("value")
        except Exception as e:  # noqa: BLE001
            print(f"  retry {i+1} for {series_id}: {e}")
            time.sleep(2 + i)
    return pd.Series(dtype=float, name="value")


def sync_fred(storage: Storage) -> None:
    for sid in FRED_SERIES:
        s = fetch_fred(sid)
        if s.empty:
            print(f"  FAIL  FRED/{sid}")
            continue
        # macro/<sid>.parquet — single-column 'value' frame indexed by date
        df = s.to_frame()
        n = storage.upsert("macro", sid, df)
        print(f"  OK    FRED/{sid:<15s}  +{n} rows, last={s.index.max().date()}")


# ---------------------------------------------------------------------------
# Extra ETFs for the 50-strategy validation
# ---------------------------------------------------------------------------
EXTRA_ETFS = [
    # Faber/Antonacci/GTAA building blocks
    "VEU", "EFA", "IEF", "VNQ", "DBC", "BIL", "BND", "AGG", "SHY",
    # Factor ETFs
    "USMV", "QUAL", "MTUM", "VLUE", "SPLV",
    # Small-cap value
    "VBR", "IJS",
    # Gold alternatives
    "GLDM",
    # 11 SPDR sector ETFs for cross-sectional momentum / reversal
    "XLK", "XLF", "XLE", "XLY", "XLP", "XLV", "XLI", "XLU", "XLB", "XLRE", "XLC",
]


def sync_etfs(storage: Storage) -> None:
    for sym in EXTRA_ETFS:
        df = fetch_yf(sym, start="2010-01-01")
        if df is None or df.empty:
            print(f"  FAIL  yf/{sym}")
            continue
        n = storage.upsert("prices", sym, df)
        last = df.index.max().date()
        print(f"  OK    yf/{sym:<6s}     +{n} rows, last={last}")


# ---------------------------------------------------------------------------
# AAII bearish % weekly — manual CSV (download from aaii.com)
# Auto-fetch is fragile; we look for a user-dropped CSV first.
# ---------------------------------------------------------------------------
def sync_aaii(storage: Storage) -> None:
    candidates = [
        ROOT / "validation50" / "data_drops" / "aaii_sentiment.csv",
        pathlib.Path("/Users/bytedance/Downloads/sentiment.csv"),
    ]
    for p in candidates:
        if not p.exists():
            continue
        try:
            df = pd.read_csv(p, skiprows=3)
            df.columns = [c.strip() for c in df.columns]
            # Common shape: Reported Date, Bullish, Neutral, Bearish, ...
            date_col = next(c for c in df.columns if "Date" in c)
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
            df = df.dropna(subset=[date_col]).set_index(date_col).sort_index()
            # Bull/Bear may be in % form already
            for c in ("Bullish", "Bearish", "Neutral"):
                if c in df.columns:
                    df[c] = pd.to_numeric(df[c], errors="coerce")
            keep = [c for c in ("Bullish", "Bearish", "Neutral") if c in df.columns]
            df = df[keep]
            storage.upsert("macro", "AAII_SENTIMENT", df)
            print(f"  OK    AAII_SENTIMENT from {p}  rows={len(df)} last={df.index.max().date()}")
            return
        except Exception as e:  # noqa: BLE001
            print(f"  AAII parse fail at {p}: {e}")
    print("  SKIP  AAII_SENTIMENT — drop CSV at validation50/data_drops/aaii_sentiment.csv")


# ---------------------------------------------------------------------------
# CBOE Put/Call ratio (daily)
# ---------------------------------------------------------------------------
CBOE_PCR_URL = "https://cdn.cboe.com/api/global/us_indices/daily_prices/CBOE_TOTAL_PC.csv"


def sync_cboe_pcr(storage: Storage) -> None:
    try:
        data = urllib.request.urlopen(CBOE_PCR_URL, timeout=15).read().decode()
        df = pd.read_csv(io.StringIO(data))
        date_col = next(c for c in df.columns if "date" in c.lower())
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.set_index(date_col).sort_index()
        storage.upsert("macro", "CBOE_PCR", df)
        print(f"  OK    CBOE_PCR  rows={len(df)} last={df.index.max().date()}")
    except Exception as e:  # noqa: BLE001
        print(f"  SKIP  CBOE_PCR — {e}")


# ---------------------------------------------------------------------------
# Shiller CAPE — multpl.com static page
# ---------------------------------------------------------------------------
def sync_shiller_cape(storage: Storage) -> None:
    try:
        url = "https://www.multpl.com/shiller-pe/table/by-month"
        html = urllib.request.urlopen(url, timeout=15).read().decode()
        # quick & dirty parse
        tables = pd.read_html(io.StringIO(html))
        df = tables[0]
        df.columns = ["date", "value"]
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["value"] = pd.to_numeric(df["value"].astype(str).str.replace("†", "")
                                    .str.strip(), errors="coerce")
        df = df.dropna().set_index("date").sort_index()
        storage.upsert("macro", "SHILLER_CAPE", df)
        print(f"  OK    SHILLER_CAPE  rows={len(df)} last={df.index.max().date()}")
    except Exception as e:  # noqa: BLE001
        print(f"  SKIP  SHILLER_CAPE — {e}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--only", type=str, default=None,
                   help="comma list: fred,etfs,aaii,pcr,cape")
    args = p.parse_args()
    tasks = set((args.only or "fred,etfs,aaii,pcr,cape").split(","))

    storage = Storage()
    if "fred" in tasks:
        print("--- FRED ---")
        sync_fred(storage)
    if "etfs" in tasks:
        print("--- ETFs ---")
        sync_etfs(storage)
    if "aaii" in tasks:
        print("--- AAII ---")
        sync_aaii(storage)
    if "pcr" in tasks:
        print("--- CBOE PCR ---")
        sync_cboe_pcr(storage)
    if "cape" in tasks:
        print("--- Shiller CAPE ---")
        sync_shiller_cape(storage)


if __name__ == "__main__":
    main()
