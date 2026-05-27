"""Daily refresh CLI.

    python -m finance_data_api.refresh                 # refresh whole universe
    python -m finance_data_api.refresh --only QQQ,VIX  # subset
    python -m finance_data_api.refresh --class qdii_etf

Each series is pulled in full (the underlying APIs are cheap & return everything)
then merged into the parquet cache. Failures are reported, never fatal — the
rest of the universe still updates.
"""
from __future__ import annotations

import argparse
import pathlib
import sys
from datetime import datetime
from typing import Optional

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from storage import Storage
from universe import UNIVERSE, Asset
import fetchers as F


def _fetch_one(asset: Asset):
    src = asset.source
    if src == "yfinance":
        return ("prices", F.fetch_yf(asset.symbol))
    if src == "ak_etf":
        return ("prices", F.fetch_ak_etf(asset.symbol))
    if src == "ak_index":
        return ("prices", F.fetch_ak_index(asset.symbol))
    if src == "ak_hk_index":
        return ("prices", F.fetch_ak_hk_index(asset.symbol))
    if src == "ak_bond_yield":
        return ("macro", F.fetch_ak_bond_yield())
    if src == "ak_north_flow":
        return ("macro", F.fetch_ak_north_flow())
    if src == "ak_ah_premium":
        return ("macro", F.fetch_ak_ah_premium())
    raise ValueError(f"unknown source: {src}")


def _fetch_extras(asset: Asset):
    out = []
    for tag in asset.extras:
        if tag == "nav":
            df = F.fetch_ak_fund_nav(asset.symbol)
            out.append(("nav", df))
    return out


def refresh(only: Optional[list[str]] = None,
            asset_class: Optional[str] = None,
            sources: Optional[list[str]] = None) -> None:
    storage = Storage()
    targets = UNIVERSE
    if only:
        targets = [a for a in targets if a.key in set(only)]
    if asset_class:
        targets = [a for a in targets if a.asset_class == asset_class]
    if sources:
        targets = [a for a in targets if a.source in set(sources)]

    ok, fail = 0, 0
    for a in targets:
        ts = datetime.now().strftime("%H:%M:%S")
        try:
            kind, df = _fetch_one(a)
            if df is None or df.empty:
                print(f"[{ts}] FAIL  {a.key:<14s} ({a.source:<14s})  empty result")
                fail += 1
            else:
                n = storage.upsert(kind, a.key, df)
                print(f"[{ts}] OK    {a.key:<14s} ({a.source:<14s})  +{n:5d} rows, last={df.index.max().date()}")
                ok += 1
            for tag, edf in _fetch_extras(a):
                if edf is None or edf.empty:
                    print(f"            extras:{tag:<5s}  empty")
                    continue
                n2 = storage.upsert(tag, a.key, edf)
                print(f"            extras:{tag:<5s}  +{n2} rows")
        except Exception as e:  # noqa: BLE001
            fail += 1
            print(f"[{ts}] ERR   {a.key:<14s} ({a.source:<14s})  {e}")

    print(f"\nDone. ok={ok} fail={fail} total={len(targets)}")


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--only", type=str, default=None, help="comma list of asset keys")
    p.add_argument("--class", dest="asset_class", type=str, default=None)
    p.add_argument("--sources", type=str, default=None, help="comma list of sources")
    args = p.parse_args(argv)
    refresh(
        only=args.only.split(",") if args.only else None,
        asset_class=args.asset_class,
        sources=args.sources.split(",") if args.sources else None,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
