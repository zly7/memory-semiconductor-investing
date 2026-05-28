"""16 — SPY breakdown >3% below SMA50: buy, hold 20 days."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import (
    daily_returns, sma, switching_returns, cash_ret_from_bil,
    threshold_event_fwd_returns, classify_verdict,
)
from .vix_above_30_buy_spy import _hold_n_after_trigger

META = StrategyMeta(
    id="spy_50d_breakdown",
    name_cn="SPY 跌破 50日 3% 反弹",
    family="mean_reversion",
    lit_verdict="mixed",
)


@register(META.id)
def compute() -> Result:
    spy = load_price("SPY")
    bil = load_price("BIL")
    ma50 = sma(spy, 50)
    dev = (spy / ma50 - 1.0)
    trig = dev < -0.03
    pos = _hold_n_after_trigger(trig.fillna(False), 20)
    cash = cash_ret_from_bil(bil, spy.index)
    spy_ret = daily_returns(spy)
    strat = switching_returns(pos, spy_ret, cash)

    bench = {"spy_buy_hold": spy_ret, "bil_cash": cash}
    buckets = threshold_event_fwd_returns(
        flag=trig.fillna(False), asset=spy,
        horizons={"5d": 5, "20d": 20, "60d": 60},
    )
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META, primary_series=dev.rename("dev to SMA50"),
        asset_series=spy, strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
        notes=f"trigger days: {int(trig.sum())} | hold 20d post-trigger",
    )
