"""17 — SPY drawdown >10% from trailing 1Y high: DCA-buy until -20% then exit."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import (
    daily_returns, switching_returns, cash_ret_from_bil,
    threshold_event_fwd_returns, classify_verdict,
)
from .vix_above_30_buy_spy import _hold_n_after_trigger

META = StrategyMeta(
    id="spy_drawdown_10pct",
    name_cn="SPY 从近 1Y 高点回撤 10% 买入",
    family="mean_reversion",
    lit_verdict="mixed",
)


@register(META.id)
def compute() -> Result:
    spy = load_price("SPY")
    bil = load_price("BIL")
    high_1y = spy.rolling(252, min_periods=60).max()
    dd = spy / high_1y - 1.0
    trig = dd < -0.10

    pos = _hold_n_after_trigger(trig.fillna(False), 120)  # hold 6 months after trigger
    cash = cash_ret_from_bil(bil, spy.index)
    spy_ret = daily_returns(spy)
    strat = switching_returns(pos, spy_ret, cash)
    bench = {"spy_buy_hold": spy_ret, "bil_cash": cash}

    buckets = threshold_event_fwd_returns(
        flag=trig.fillna(False), asset=spy,
        horizons={"20d": 20, "60d": 60, "120d": 120, "252d": 252},
    )
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META, primary_series=dd.rename("drawdown from 1Y high"),
        asset_series=spy, strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
        notes=f"trigger days: {int(trig.sum())} | hold 120d post-trigger",
    )
