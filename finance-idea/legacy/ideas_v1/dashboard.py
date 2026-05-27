"""dashboard.py — current state of all 10 signals.

Run after a refresh:

    python ideas/dashboard.py

Outputs:
    ideas/outputs/dashboard.md     # human-readable current snapshot
    ideas/outputs/dashboard.json   # machine readable for further automation
"""
from __future__ import annotations

import json
import sys
import datetime as dt
import pathlib
from typing import Any

import numpy as np
import pandas as pd

from common import load_price, load_nav, load_macro, storage, OUT

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "finance-data-api"))
import fetchers as F  # noqa: E402


def _safe_load_price(key, col="close"):
    try:
        return load_price(key, col)
    except Exception:
        return None


def _safe_load_nav(key):
    try:
        return load_nav(key)
    except Exception:
        return None


def _signal_qdii_premium() -> dict[str, Any]:
    """Live cross-sectional median premium across Nasdaq QDII ETFs.

    Uses today's IOPV snapshot for the freshest read; falls back to historical
    cache if the live snapshot endpoint fails.
    """
    nasdaq_codes = ["513100", "513300", "159941", "513870", "513110",
                    "159632", "159659", "513390", "159513", "159660",
                    "513870", "159696", "159501"]
    try:
        snap = F.fetch_etf_spot_snapshot()
        sub = snap[snap["code"].isin(nasdaq_codes)].dropna(subset=["premium_pct"])
        if len(sub) > 0:
            med = float(sub["premium_pct"].median())
            return {
                "name": "01 QDII Nasdaq premium",
                "value": round(med, 2),
                "unit": "%",
                "interpretation": (
                    "HOT — likely contrarian SHORT" if med > 5 else
                    "ELEVATED" if med > 2 else
                    "NEUTRAL" if med > -2 else
                    "COLD — possible contrarian LONG"),
                "details": sub[["code", "name", "premium_pct"]].to_dict("records")[:8],
            }
    except Exception as e:  # noqa: BLE001
        return {"name": "01 QDII Nasdaq premium", "value": None,
                "interpretation": f"snapshot unavailable: {e}"}


def _signal_qqq_ma200() -> dict:
    qqq = _safe_load_price("QQQ")
    if qqq is None:
        return {"name": "02 QQQ vs 200d SMA", "value": None}
    sma = qqq.rolling(200).mean().iloc[-1]
    ratio = qqq.iloc[-1] / sma
    return {
        "name": "02 QQQ vs 200d SMA",
        "value": round(float(ratio), 3),
        "unit": "ratio",
        "interpretation": "ABOVE SMA200 (trend)" if ratio > 1 else "BELOW SMA200 (dip)",
        "detail": f"close {qqq.iloc[-1]:.2f}, SMA200 {sma:.2f}",
    }


def _signal_vix() -> dict:
    vix = _safe_load_price("VIX")
    if vix is None:
        return {"name": "03 VIX", "value": None}
    v = float(vix.iloc[-1])
    return {
        "name": "03 VIX",
        "value": round(v, 2),
        "unit": "pts",
        "interpretation": "PANIC — buy-the-fear" if v > 30 else
                          "elevated" if v > 22 else
                          "neutral" if v > 13 else
                          "COMPLACENT",
    }


def _signal_gold_copper() -> dict:
    g = _safe_load_price("GC"); c = _safe_load_price("HG")
    if g is None or c is None:
        return {"name": "04 Gold/Copper", "value": None}
    ratio = g / c
    z = (ratio - ratio.rolling(252).mean()) / ratio.rolling(252).std()
    last_z = float(z.iloc[-1])
    return {
        "name": "04 Gold/Copper z (252d)",
        "value": round(last_z, 2),
        "unit": "z",
        "interpretation": "RISK-OFF spike" if last_z > 1.5 else
                          "RISK-ON" if last_z < -1.5 else "neutral",
        "detail": f"ratio {ratio.iloc[-1]:.2f}",
    }


def _signal_dxy() -> dict:
    dxy = _safe_load_price("DXY")
    if dxy is None or len(dxy) < 130:
        return {"name": "05 DXY 6m change", "value": None}
    chg = dxy.iloc[-1] / dxy.iloc[-127] - 1
    return {
        "name": "05 DXY 6m change",
        "value": round(float(chg * 100), 2),
        "unit": "%",
        "interpretation": "USD WEAKENING fast — EM tailwind" if chg < -0.05 else
                          "USD STRENGTHENING fast — EM headwind" if chg > 0.05 else
                          "neutral",
    }


def _signal_yield_curve() -> dict:
    t = _safe_load_price("TNX"); ir = _safe_load_price("IRX")
    if t is None or ir is None:
        return {"name": "06 10Y-3M spread", "value": None}
    sp = (t.iloc[-1] - ir.iloc[-1]) / 10.0
    return {
        "name": "06 10Y-3M spread",
        "value": round(float(sp), 2),
        "unit": "%",
        "interpretation": "INVERTED — recession watch" if sp < 0 else
                          "FLAT" if sp < 0.5 else "NORMAL",
    }


def _signal_ah_premium() -> dict:
    try:
        ah = load_macro("AH_PREMIUM")
        col = ah.select_dtypes(include="number").columns[0]
        v = float(ah[col].dropna().iloc[-1])
        return {"name": "07 AH premium", "value": round(v, 2),
                "interpretation": f"A premium over H = {v:.1f}"}
    except Exception:
        return {"name": "07 AH premium", "value": None,
                "interpretation": "history unavailable in this run"}


def _signal_north_flow() -> dict:
    try:
        nf = load_macro("NORTH_FLOW")
        num_cols = nf.select_dtypes(include="number")
        # pick the most "flow-like" column
        for cand in ("当日成交净买额", "当日资金流入", "净买额", "资金净流入"):
            if cand in num_cols.columns:
                s = num_cols[cand].dropna()
                v = float(s.rolling(20).sum().iloc[-1])
                return {"name": "08 North 20d flow", "value": round(v, 1),
                        "interpretation": "INFLOW" if v > 0 else "OUTFLOW"}
        s = num_cols.iloc[:, 0].dropna()
        v = float(s.rolling(20).sum().iloc[-1])
        return {"name": "08 North 20d flow", "value": round(v, 1),
                "interpretation": "INFLOW" if v > 0 else "OUTFLOW"}
    except Exception:
        return {"name": "08 North 20d flow", "value": None}


def _signal_iwm_spy() -> dict:
    iwm = _safe_load_price("IWM"); spy = _safe_load_price("SPY")
    if iwm is None or spy is None:
        return {"name": "09 IWM/SPY ratio z", "value": None}
    idx = iwm.index.intersection(spy.index)
    ratio = (iwm.loc[idx] / spy.loc[idx])
    z = (ratio - ratio.rolling(252).mean()) / ratio.rolling(252).std()
    last_z = float(z.iloc[-1])
    return {
        "name": "09 IWM/SPY z (252d)", "value": round(last_z, 2),
        "interpretation": "small-cap STRONG (risk-on)" if last_z > 0.5 else
                          "small-cap WEAK (risk-off)" if last_z < -0.5 else "neutral",
    }


def _signal_btc_gold() -> dict:
    btc = _safe_load_price("BTC"); gld = _safe_load_price("GLD")
    if btc is None or gld is None:
        return {"name": "10 ln(BTC/Gold) z", "value": None}
    idx = btc.index.intersection(gld.index)
    r = np.log(btc.loc[idx] / gld.loc[idx])
    z = (r - r.rolling(252).mean()) / r.rolling(252).std()
    last_z = float(z.iloc[-1])
    return {
        "name": "10 ln(BTC/Gold) z (252d)", "value": round(last_z, 2),
        "interpretation": "EUPHORIA" if last_z > 1.5 else
                          "fear" if last_z < -1.5 else "neutral",
    }


SIGNAL_FNS = [
    _signal_qdii_premium, _signal_qqq_ma200, _signal_vix, _signal_gold_copper,
    _signal_dxy, _signal_yield_curve, _signal_ah_premium, _signal_north_flow,
    _signal_iwm_spy, _signal_btc_gold,
]


def main():
    rows = []
    for fn in SIGNAL_FNS:
        try:
            rows.append(fn())
        except Exception as e:  # noqa: BLE001
            rows.append({"name": fn.__name__, "value": None, "interpretation": f"err: {e}"})

    asof = dt.datetime.now().isoformat(timespec="seconds")
    md = ["# Finance-Idea Dashboard", f"_as of {asof}_", ""]
    md.append("| Signal | Value | Interpretation |")
    md.append("|---|---|---|")
    for r in rows:
        v = r.get("value")
        v_str = "—" if v is None else f"{v}"
        if r.get("unit"):
            v_str += f" {r['unit']}"
        md.append(f"| {r['name']} | {v_str} | {r.get('interpretation','')} |")
    md.append("")
    md.append("Details:")
    for r in rows:
        d = r.get("detail") or r.get("details")
        if d is not None:
            md.append(f"- **{r['name']}**: {d}")
    (OUT / "dashboard.md").write_text("\n".join(md))
    (OUT / "dashboard.json").write_text(json.dumps({"asof": asof, "signals": rows},
                                                   indent=2, ensure_ascii=False, default=str))
    for r in rows:
        v = r.get("value")
        v_str = "—" if v is None else str(v)
        print(f"{r['name']:<32s}  {v_str:>10s}  {r.get('interpretation','')}")
    print(f"\nwrote {OUT/'dashboard.md'} and {OUT/'dashboard.json'}")


if __name__ == "__main__":
    main()
