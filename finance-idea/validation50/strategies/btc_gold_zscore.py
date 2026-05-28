"""35 — BTC/Gold log-ratio z-score: extreme risk-appetite signal vs SPY fwd."""
import numpy as np
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import (
    daily_returns, rolling_z, switching_returns, cash_ret_from_bil,
    classify_verdict, bucket_fwd_returns, bucket_monotonicity,
)

META = StrategyMeta(
    id="btc_gold_zscore",
    name_cn="BTC/黄金 情绪 z",
    family="cross_asset",
    lit_verdict="mixed",
)


@register(META.id)
def compute() -> Result:
    btc = load_price("BTC")
    gld = load_price("GLD")
    spy = load_price("SPY")
    bil = load_price("BIL")
    common = btc.index.intersection(gld.index).intersection(spy.index)
    btc, gld, spy = btc.loc[common], gld.loc[common], spy.loc[common]

    ratio = np.log(btc / gld)
    z = rolling_z(ratio, 252)

    # z > 1.5 → euphoria (risk-off SPY → cash); z < -1.5 → fear (risk-on SPY)
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
        meta=META, primary_series=z.rename("ln(BTC/Gold) z (252d)"),
        asset_series=spy, strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
    )
