"""36 — Gold/silver ratio extremes (GLD/SLV) → SPY tilt."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import (
    daily_returns, rolling_z, switching_returns, cash_ret_from_bil,
    classify_verdict, bucket_fwd_returns, bucket_monotonicity,
)

META = StrategyMeta(
    id="gold_silver_ratio",
    name_cn="金银比 (GLD/SLV) 极值",
    family="cross_asset",
    lit_verdict="mixed",
)


@register(META.id)
def compute() -> Result:
    gld = load_price("GLD")
    slv = load_price("SLV")
    spy = load_price("SPY")
    bil = load_price("BIL")
    common = gld.index.intersection(slv.index).intersection(spy.index)
    gld, slv, spy = gld.loc[common], slv.loc[common], spy.loc[common]
    ratio = gld / slv
    z = rolling_z(ratio, 252)

    pos = pd.Series(0.5, index=spy.index)
    pos[z > 1.5] = 0.0  # risk-aversion (gold relatively expensive) → cash
    pos[z < -1.5] = 1.0  # risk appetite → full SPY
    cash = cash_ret_from_bil(bil, spy.index)
    spy_ret = daily_returns(spy)
    strat = switching_returns(pos, spy_ret, cash)
    bench = {"spy_buy_hold": spy_ret, "bil_cash": cash}
    buckets = bucket_fwd_returns(z.dropna(), spy, {"20d": 20, "60d": 60, "120d": 120})
    mono = bucket_monotonicity(buckets)
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]),
                                    direction_check=-mono)
    return Result(
        meta=META, primary_series=z.rename("GLD/SLV z (252d)"),
        asset_series=spy, strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
    )
