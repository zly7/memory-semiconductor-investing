"""22 — Northbound flow 20-day cumulative: long CSI300 when net inflows positive."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats, load_macro_value
from ._storage_helpers import load_macro_df
from ._helpers import (
    daily_returns, switching_returns, classify_verdict,
    bucket_fwd_returns, bucket_monotonicity,
)

META = StrategyMeta(
    id="northbound_flow",
    name_cn="北向资金 20日累计 → 沪深300",
    family="sentiment",
    lit_verdict="mixed",
)


def _pick_flow_col(df: pd.DataFrame) -> str:
    for c in ("当日成交净买额", "当日资金流入", "净买额", "资金净流入"):
        if c in df.columns:
            return c
    return df.select_dtypes(include="number").columns[0]


@register(META.id)
def compute() -> Result:
    df = load_macro_df("NORTH_FLOW")
    flow = df[_pick_flow_col(df)].dropna().astype(float)
    cum20 = flow.rolling(20).sum().dropna()

    csi = load_price("CSI300").reindex(cum20.index).ffill().dropna()
    common = cum20.index.intersection(csi.index)
    cum20, csi = cum20.loc[common], csi.loc[common]
    csi_ret = daily_returns(csi)

    y = load_macro_value("DGS3MO").reindex(csi.index).ffill()
    cash = (y / 100.0 / 252.0).fillna(0.0)

    flag = (cum20 > 0).astype(float)
    strat = switching_returns(flag, csi_ret, cash)
    bench = {"csi300_buy_hold": csi_ret, "cash_3m": cash}
    buckets = bucket_fwd_returns(cum20, csi, {"20d": 20, "60d": 60, "120d": 120})
    mono = bucket_monotonicity(buckets)
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["csi300_buy_hold"]),
                                    direction_check=mono)
    return Result(
        meta=META, primary_series=cum20.rename("20d cum flow (亿)"),
        asset_series=csi, strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
        notes=f"bucket ρ={mono:+.2f}; long CSI300 when 20d cum > 0",
    )
