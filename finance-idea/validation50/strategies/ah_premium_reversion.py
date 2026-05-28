"""23 — AH premium reversion. DATA UNAVAILABLE (akshare endpoint broken)."""
import pandas as pd
from runner import StrategyMeta, Result, register

META = StrategyMeta(
    id="ah_premium_reversion",
    name_cn="AH 溢价指数反转",
    family="sentiment",
    lit_verdict="mixed",
)


@register(META.id)
def compute() -> Result:
    return Result(
        meta=META,
        primary_series=pd.Series(dtype=float),
        verdict="skipped",
        verdict_why="AH premium index unavailable — akshare stock_hk_ah_premium_index endpoint broken",
        notes="see FEATURE_LIST.md row 23 — needs replacement data source",
    )
