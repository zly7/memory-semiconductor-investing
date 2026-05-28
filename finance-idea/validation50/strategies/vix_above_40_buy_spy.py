"""20 — VIX > 40 contrarian buy SPY (rarer, deeper crisis trigger)."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import (
    daily_returns, switching_returns, cash_ret_from_bil,
    threshold_event_fwd_returns, classify_verdict,
)
from .vix_above_30_buy_spy import _hold_n_after_trigger

META = StrategyMeta(
    id="vix_above_40_buy_spy",
    name_cn="VIX > 40 强抄底 SPY",
    family="sentiment",
    lit_verdict="robust",
)


@register(META.id)
def compute() -> Result:
    vix = load_price("VIX")
    spy = load_price("SPY")
    bil = load_price("BIL")

    common = vix.index.intersection(spy.index)
    vix = vix.loc[common]
    spy = spy.loc[common]
    cash = cash_ret_from_bil(bil, spy.index)
    spy_ret = daily_returns(spy)

    trigger = vix > 40.0
    pos = _hold_n_after_trigger(trigger, 120)  # longer hold for deeper trigger
    strat = switching_returns(pos, spy_ret, cash)
    bench = {"spy_buy_hold": spy_ret, "bil_cash": cash}

    buckets = threshold_event_fwd_returns(
        flag=trigger, asset=spy,
        horizons={"20d": 20, "60d": 60, "120d": 120, "252d": 252},
    )
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META, primary_series=vix, asset_series=spy,
        strategy_returns=strat, benchmark_returns=bench,
        buckets=buckets, verdict=verdict, verdict_why=why,
        notes=f"trigger days: {int(trigger.sum())} | in-market days: {int(pos.sum())}",
    )
