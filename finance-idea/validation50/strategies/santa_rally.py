"""40 — Santa Claus Rally: last 5 trading days of Dec + first 2 of Jan."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import (
    daily_returns, switching_returns, cash_ret_from_bil, classify_verdict,
)

META = StrategyMeta(
    id="santa_rally",
    name_cn="Santa Claus Rally",
    family="seasonal",
    lit_verdict="seasonal-window-only",
)


def _santa_window(index: pd.DatetimeIndex) -> pd.Series:
    """Boolean: True on last 5 trading days of December + first 2 of January."""
    flag = pd.Series(False, index=index)
    for year in sorted(set(index.year)):
        dec = index[(index.year == year) & (index.month == 12)]
        if len(dec) >= 5:
            flag.loc[dec[-5:]] = True
        jan = index[(index.year == year) & (index.month == 1)]
        if len(jan) >= 2:
            flag.loc[jan[:2]] = True
    return flag


@register(META.id)
def compute() -> Result:
    spy = load_price("SPY")
    bil = load_price("BIL")
    pos = _santa_window(spy.index).astype(float)
    spy_ret = daily_returns(spy)
    cash = cash_ret_from_bil(bil, spy.index)
    strat = switching_returns(pos, spy_ret, cash)
    bench = {"spy_buy_hold": spy_ret, "bil_cash": cash}
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META, primary_series=pos.rename("santa_window"),
        asset_series=spy, strategy_returns=strat, benchmark_returns=bench,
        verdict=verdict, verdict_why=why,
        notes=f"window days/year ≈ 7; in-market days total: {int(pos.sum())}",
    )
