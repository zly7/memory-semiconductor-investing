"""42 — Pre-FOMC drift. DATA UNAVAILABLE (no FOMC schedule cached)."""
import pandas as pd
from runner import StrategyMeta, Result, register

META = StrategyMeta(
    id="prefomc_drift",
    name_cn="Pre-FOMC 漂移",
    family="seasonal",
    lit_verdict="decayed",
)


@register(META.id)
def compute() -> Result:
    return Result(
        meta=META,
        primary_series=pd.Series(dtype=float),
        verdict="skipped",
        verdict_why="FOMC schedule not in cache — would need calendar from Federal Reserve site",
        notes="see FEATURE_LIST.md row 42",
    )
