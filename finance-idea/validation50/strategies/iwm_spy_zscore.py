"""34 — IWM/SPY relative-strength z-score: rotate small ↔ large at extremes."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import (
    daily_returns, rolling_z, classify_verdict, bucket_fwd_returns,
    bucket_monotonicity,
)

META = StrategyMeta(
    id="iwm_spy_zscore",
    name_cn="IWM/SPY 相对强度 z",
    family="cross_asset",
    lit_verdict="mixed",
)


@register(META.id)
def compute() -> Result:
    iwm = load_price("IWM")
    spy = load_price("SPY")
    common = iwm.index.intersection(spy.index)
    iwm, spy = iwm.loc[common], spy.loc[common]
    ratio = iwm / spy
    z = rolling_z(ratio, 252)

    iwm_ret = daily_returns(iwm)
    spy_ret = daily_returns(spy)
    # z > 1.5 → IWM rich, tilt SPY; z < -1.5 → IWM cheap, tilt IWM; else 50/50
    w_iwm = pd.Series(0.5, index=spy.index)
    w_iwm[z > 1.5] = 0.0
    w_iwm[z < -1.5] = 1.0
    w_spy = 1.0 - w_iwm
    strat = (w_iwm.shift(1).fillna(0.5) * iwm_ret
             + w_spy.shift(1).fillna(0.5) * spy_ret).astype(float)
    bench = {"spy_buy_hold": spy_ret, "iwm_buy_hold": iwm_ret,
             "eq_50_50": 0.5 * spy_ret + 0.5 * iwm_ret}
    buckets = bucket_fwd_returns(z.dropna(), iwm / spy,
                                 {"20d": 20, "60d": 60, "120d": 120})
    mono = bucket_monotonicity(buckets)
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["eq_50_50"]),
                                    direction_check=-mono)
    return Result(
        meta=META, primary_series=z.rename("IWM/SPY z (252d)"),
        asset_series=ratio, strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
    )
