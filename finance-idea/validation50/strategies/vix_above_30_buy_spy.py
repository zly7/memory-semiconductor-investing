"""19 — VIX > 30 contrarian buy SPY (hold 60d after each trigger)."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import (
    daily_returns, switching_returns, cash_ret_from_bil,
    threshold_event_fwd_returns, classify_verdict,
)

META = StrategyMeta(
    id="vix_above_30_buy_spy",
    name_cn="VIX > 30 抄底 SPY",
    family="sentiment",
    lit_verdict="robust",
)

VIX_THRESHOLD = 30.0
HOLD_DAYS = 60


def _hold_n_after_trigger(flag: pd.Series, n: int) -> pd.Series:
    """Return a 0/1 position series that is 1 for n trading days after each
    True in `flag`."""
    pos = pd.Series(0, index=flag.index, dtype=float)
    countdown = 0
    for d in flag.index:
        if bool(flag.loc[d]):
            countdown = n
        pos.loc[d] = 1.0 if countdown > 0 else 0.0
        if countdown > 0:
            countdown -= 1
    return pos


@register(META.id)
def compute() -> Result:
    vix = load_price("VIX")
    spy = load_price("SPY")
    bil = load_price("BIL")

    common = vix.index.intersection(spy.index)
    vix = vix.loc[common]
    spy = spy.loc[common]

    trigger = vix > VIX_THRESHOLD
    pos = _hold_n_after_trigger(trigger, HOLD_DAYS)
    cash = cash_ret_from_bil(bil, spy.index)
    spy_ret = daily_returns(spy)
    strat = switching_returns(pos, spy_ret, cash)

    bench = {"spy_buy_hold": spy_ret, "bil_cash": cash}

    buckets = threshold_event_fwd_returns(
        flag=trigger,
        asset=spy,
        horizons={"20d": 20, "60d": 60, "120d": 120, "252d": 252},
    )
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META,
        primary_series=vix,
        asset_series=spy,
        strategy_returns=strat,
        benchmark_returns=bench,
        buckets=buckets,
        verdict=verdict,
        verdict_why=why,
        notes=f"in-market days: {int(pos.sum())}/{len(pos)}",
    )
