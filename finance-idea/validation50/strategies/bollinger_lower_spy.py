"""13 — Bollinger lower-band oversold mean reversion (SPY)."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import (
    daily_returns, sma, switching_returns, cash_ret_from_bil,
    threshold_event_fwd_returns, classify_verdict,
)

META = StrategyMeta(
    id="bollinger_lower_spy",
    name_cn="SPY 布林下轨反弹",
    family="mean_reversion",
    lit_verdict="mixed",
)


@register(META.id)
def compute() -> Result:
    spy = load_price("SPY")
    bil = load_price("BIL")
    n = 20
    ma = sma(spy, n)
    sd = spy.rolling(n).std()
    lower = ma - 2 * sd

    below = (spy < lower)
    pos = pd.Series(0.0, index=spy.index)
    holding = False
    for d in spy.index:
        if not holding and (not pd.isna(below.loc[d])) and bool(below.loc[d]):
            holding = True
        elif holding and (not pd.isna(ma.loc[d])) and spy.loc[d] > ma.loc[d]:
            holding = False
        pos.loc[d] = 1.0 if holding else 0.0

    cash = cash_ret_from_bil(bil, spy.index)
    spy_ret = daily_returns(spy)
    strat = switching_returns(pos, spy_ret, cash)
    bench = {"spy_buy_hold": spy_ret, "bil_cash": cash}

    buckets = threshold_event_fwd_returns(
        flag=below.fillna(False), asset=spy,
        horizons={"5d": 5, "20d": 20, "60d": 60},
    )
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META, primary_series=((spy - ma) / sd).rename("zscore"),
        asset_series=spy, strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
        notes=f"in-market days: {int(pos.sum())} | bands 20d ±2σ",
    )
