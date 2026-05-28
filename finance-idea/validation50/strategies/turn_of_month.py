"""41 — Turn-of-month effect: last 1 + first 3 trading days of each month."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import (
    daily_returns, switching_returns, cash_ret_from_bil, classify_verdict,
)

META = StrategyMeta(
    id="turn_of_month",
    name_cn="月末效应",
    family="seasonal",
    lit_verdict="seasonal-window-only",
)


def _turn_window(index: pd.DatetimeIndex) -> pd.Series:
    flag = pd.Series(False, index=index)
    by_ym = pd.Series(index, index=index).groupby([index.year, index.month])
    days_per_month = by_ym.apply(lambda s: s.index.tolist())
    months = sorted(days_per_month.keys())
    for i, ym in enumerate(months):
        days = days_per_month[ym]
        if len(days) >= 1:
            flag.loc[days[-1]] = True
        if i + 1 < len(months):
            nxt = days_per_month[months[i + 1]]
            for d in nxt[:3]:
                flag.loc[d] = True
    return flag


@register(META.id)
def compute() -> Result:
    spy = load_price("SPY")
    bil = load_price("BIL")
    pos = _turn_window(spy.index).astype(float)
    spy_ret = daily_returns(spy)
    cash = cash_ret_from_bil(bil, spy.index)
    strat = switching_returns(pos, spy_ret, cash)
    bench = {"spy_buy_hold": spy_ret, "bil_cash": cash}
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META, primary_series=pos.rename("turn_window"),
        asset_series=spy, strategy_returns=strat, benchmark_returns=bench,
        verdict=verdict, verdict_why=why,
        notes=f"window days/month ≈ 4; in-market total: {int(pos.sum())}",
    )
