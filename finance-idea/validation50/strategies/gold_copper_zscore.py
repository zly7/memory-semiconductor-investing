"""33 — Gold/copper ratio z-score extremes → equity risk tilt."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import (
    daily_returns, rolling_z, switching_returns, cash_ret_from_bil,
    classify_verdict, bucket_fwd_returns, bucket_monotonicity,
)

META = StrategyMeta(
    id="gold_copper_zscore",
    name_cn="金铜比 z-score 极值",
    family="macro",
    lit_verdict="mixed",
)


@register(META.id)
def compute() -> Result:
    gc = load_price("GC")
    hg = load_price("HG")
    spy = load_price("SPY")
    bil = load_price("BIL")
    common = gc.index.intersection(hg.index).intersection(spy.index)
    gc, hg, spy = gc.loc[common], hg.loc[common], spy.loc[common]

    ratio = (gc / hg).dropna()
    z = rolling_z(ratio, 252)
    # z > 1.5 → risk-off (cash); z < -1.5 → risk-on (full SPY); else 50/50
    pos = pd.Series(0.5, index=spy.index)
    pos[z > 1.5] = 0.0
    pos[z < -1.5] = 1.0
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
        meta=META, primary_series=z.rename("Au/Cu z-score (252d)"),
        asset_series=spy, strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
    )
