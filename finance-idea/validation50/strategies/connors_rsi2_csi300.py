"""12 — Connors RSI(2) on CSI300."""
import pandas as pd
import numpy as np
from runner import StrategyMeta, Result, register, load_price, stats, load_macro_value
from ._helpers import (
    daily_returns, sma, switching_returns, bucket_fwd_returns,
    classify_verdict, bucket_monotonicity,
)
from .connors_rsi2_spy import _rsi

META = StrategyMeta(
    id="connors_rsi2_csi300",
    name_cn="RSI(2) 沪深300",
    family="mean_reversion",
    lit_verdict="mixed",
)


@register(META.id)
def compute() -> Result:
    csi = load_price("CSI300")
    sma250 = sma(csi, 250)
    rsi2 = _rsi(csi, 2)
    long_trig = (csi > sma250) & (rsi2 < 5)
    exit_trig = rsi2 > 65
    pos = pd.Series(0.0, index=csi.index)
    holding = False
    for d in csi.index:
        lt = long_trig.loc[d]
        et = exit_trig.loc[d]
        if not holding and (not pd.isna(lt)) and bool(lt):
            holding = True
        elif holding and (not pd.isna(et)) and bool(et):
            holding = False
        pos.loc[d] = 1.0 if holding else 0.0

    y = load_macro_value("DGS3MO").reindex(csi.index).ffill()
    cash = (y / 100.0 / 252.0).fillna(0.0)
    csi_ret = daily_returns(csi)
    strat = switching_returns(pos, csi_ret, cash)
    bench = {"csi300_buy_hold": csi_ret, "cash_3m": cash}

    buckets = bucket_fwd_returns(
        signal=rsi2.dropna(), asset=csi,
        horizons={"5d": 5, "20d": 20, "60d": 60},
    )
    mono = bucket_monotonicity(buckets)
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["csi300_buy_hold"]),
                                    direction_check=-mono)
    return Result(
        meta=META, primary_series=rsi2, asset_series=csi,
        strategy_returns=strat, benchmark_returns=bench, buckets=buckets,
        verdict=verdict, verdict_why=why,
        notes=f"days in market: {int(pos.sum())} | bucket ρ={mono:+.2f}",
    )
