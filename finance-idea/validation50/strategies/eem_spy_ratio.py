"""38 — EEM/SPY relative-strength z-score: rotate EM ↔ US at extremes."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import (
    daily_returns, rolling_z, classify_verdict, bucket_fwd_returns,
    bucket_monotonicity,
)

META = StrategyMeta(
    id="eem_spy_ratio",
    name_cn="EEM/SPY 相对强度 z",
    family="cross_asset",
    lit_verdict="mixed",
)


@register(META.id)
def compute() -> Result:
    eem = load_price("EEM")
    spy = load_price("SPY")
    common = eem.index.intersection(spy.index)
    eem, spy = eem.loc[common], spy.loc[common]
    ratio = eem / spy
    z = rolling_z(ratio, 252)

    eem_ret = daily_returns(eem)
    spy_ret = daily_returns(spy)
    w_eem = pd.Series(0.5, index=spy.index)
    w_eem[z > 1.5] = 0.0  # EM rich → tilt US
    w_eem[z < -1.5] = 1.0  # EM cheap → tilt EM
    w_spy = 1.0 - w_eem
    strat = (w_eem.shift(1).fillna(0.5) * eem_ret
             + w_spy.shift(1).fillna(0.5) * spy_ret).astype(float)
    bench = {"spy_buy_hold": spy_ret, "eem_buy_hold": eem_ret,
             "eq_50_50": 0.5 * spy_ret + 0.5 * eem_ret}
    buckets = bucket_fwd_returns(z.dropna(), ratio,
                                 {"20d": 20, "60d": 60, "120d": 120})
    mono = bucket_monotonicity(buckets)
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["eq_50_50"]),
                                    direction_check=-mono)
    return Result(
        meta=META, primary_series=z.rename("EEM/SPY z (252d)"),
        asset_series=ratio, strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
    )
