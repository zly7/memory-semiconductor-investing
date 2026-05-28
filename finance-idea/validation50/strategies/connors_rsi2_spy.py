"""11 — Larry Connors RSI(2) on SPY (oversold long, exit on overbought)."""
import pandas as pd
import numpy as np
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import (
    daily_returns, sma, switching_returns, cash_ret_from_bil,
    bucket_fwd_returns, classify_verdict, bucket_monotonicity,
)

META = StrategyMeta(
    id="connors_rsi2_spy",
    name_cn="Larry Connors RSI(2) SPY",
    family="mean_reversion",
    lit_verdict="decayed",
)


def _rsi(price: pd.Series, n: int) -> pd.Series:
    d = price.diff()
    up = d.clip(lower=0).rolling(n).mean()
    down = (-d.clip(upper=0)).rolling(n).mean()
    rs = up / down.replace(0, np.nan)
    return 100 - 100 / (1 + rs)


@register(META.id)
def compute() -> Result:
    spy = load_price("SPY")
    bil = load_price("BIL")
    sma200 = sma(spy, 200)
    rsi2 = _rsi(spy, 2)

    long_trigger = (spy > sma200) & (rsi2 < 5)
    exit_trigger = rsi2 > 65

    pos = pd.Series(0.0, index=spy.index)
    holding = False
    for d in spy.index:
        if not holding and bool(long_trigger.loc[d]) if not pd.isna(long_trigger.loc[d]) else False:
            holding = True
        elif holding and bool(exit_trigger.loc[d]) if not pd.isna(exit_trigger.loc[d]) else False:
            holding = False
        pos.loc[d] = 1.0 if holding else 0.0

    cash = cash_ret_from_bil(bil, spy.index)
    spy_ret = daily_returns(spy)
    strat = switching_returns(pos, spy_ret, cash)
    bench = {"spy_buy_hold": spy_ret, "bil_cash": cash}

    buckets = bucket_fwd_returns(
        signal=rsi2.dropna(), asset=spy,
        horizons={"5d": 5, "20d": 20, "60d": 60},
    )
    mono = bucket_monotonicity(buckets)
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]),
                                    direction_check=-mono)  # expect inverse: low RSI → high fwd ret
    return Result(
        meta=META, primary_series=rsi2, asset_series=spy,
        strategy_returns=strat, benchmark_returns=bench, buckets=buckets,
        verdict=verdict, verdict_why=why,
        notes=f"days in market: {int(pos.sum())} | bucket ρ={mono:+.2f} (expect negative)",
    )
