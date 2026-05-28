"""30 — Shiller CAPE in top decile → reduce SPY to 50%. DATA-NEEDED."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._storage_helpers import load_macro_df
from ._helpers import daily_returns, cash_ret_from_bil, classify_verdict

META = StrategyMeta(
    id="cape_top_decile",
    name_cn="CAPE 历史最高 10% 减仓",
    family="macro",
    lit_verdict="seasonal-window-only",
)


@register(META.id)
def compute() -> Result:
    try:
        cape_df = load_macro_df("SHILLER_CAPE")
    except FileNotFoundError:
        return Result(
            meta=META, primary_series=pd.Series(dtype=float),
            verdict="skipped",
            verdict_why="Shiller CAPE not cached — run data_acq.py --only cape",
        )

    cape = cape_df["value"].dropna().astype(float)
    spy = load_price("SPY")
    bil = load_price("BIL")
    daily_cape = cape.reindex(spy.index).ffill()
    p90 = daily_cape.expanding(252).quantile(0.90)
    expensive = (daily_cape > p90).astype(float)
    pos = 1.0 - 0.5 * expensive
    cash = cash_ret_from_bil(bil, spy.index)
    spy_ret = daily_returns(spy)
    strat = (pos.shift(1).fillna(1.0) * spy_ret
             + (1.0 - pos.shift(1).fillna(1.0)) * cash).astype(float)
    bench = {"spy_buy_hold": spy_ret}
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META, primary_series=daily_cape.rename("Shiller CAPE"),
        asset_series=spy, strategy_returns=strat, benchmark_returns=bench,
        verdict=verdict, verdict_why=why,
    )
