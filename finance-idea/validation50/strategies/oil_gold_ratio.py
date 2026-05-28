"""37 — Oil/gold ratio (CL/GC) z-score vs SPY fwd return."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import (
    daily_returns, rolling_z, switching_returns, cash_ret_from_bil,
    classify_verdict, bucket_fwd_returns, bucket_monotonicity,
)

META = StrategyMeta(
    id="oil_gold_ratio",
    name_cn="油金比 (CL/GC) z 极值",
    family="cross_asset",
    lit_verdict="mixed",
)


@register(META.id)
def compute() -> Result:
    cl = load_price("CL")
    gc = load_price("GC")
    spy = load_price("SPY")
    bil = load_price("BIL")
    common = cl.index.intersection(gc.index).intersection(spy.index)
    cl, gc, spy = cl.loc[common], gc.loc[common], spy.loc[common]
    ratio = cl / gc
    z = rolling_z(ratio, 252)

    # Higher oil vs gold → reflation/growth → risk-on; lower → risk-off
    pos = pd.Series(0.5, index=spy.index)
    pos[z < -1.5] = 0.0
    pos[z > 1.5] = 1.0
    cash = cash_ret_from_bil(bil, spy.index)
    spy_ret = daily_returns(spy)
    strat = switching_returns(pos, spy_ret, cash)
    bench = {"spy_buy_hold": spy_ret, "bil_cash": cash}
    buckets = bucket_fwd_returns(z.dropna(), spy, {"20d": 20, "60d": 60, "120d": 120})
    mono = bucket_monotonicity(buckets)
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]),
                                    direction_check=mono)
    return Result(
        meta=META, primary_series=z.rename("CL/GC z (252d)"),
        asset_series=spy, strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
    )
