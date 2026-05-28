"""09 — A-share-listed QDII basket: long top-3 by 12M return, monthly."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import daily_returns, classify_verdict

META = StrategyMeta(
    id="qdii_basket_mom",
    name_cn="A 股 QDII 篮子动量",
    family="trend",
    lit_verdict="mixed",
)

QDIIS = ["QDII513100", "QDII513300", "QDII159941", "QDII513500",
         "QDII513030", "QDII513880", "QDII164906"]


@register(META.id)
def compute() -> Result:
    px_dict = {}
    for s in QDIIS:
        try:
            px_dict[s] = load_price(s)
        except FileNotFoundError:
            continue
    common = None
    for s in px_dict.values():
        common = s.index if common is None else common.intersection(s.index)
    px = pd.DataFrame({k: v.loc[common] for k, v in px_dict.items()})
    rets = px.pct_change().fillna(0.0)
    mom = px.pct_change(252)
    monthly_idx = px.resample("M").last().index

    pos = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    current = pd.Series(0.0, index=px.columns)
    for d in px.index:
        if d in monthly_idx:
            m = mom.loc[d].dropna()
            if len(m) >= 3:
                top3 = m.sort_values(ascending=False).head(3).index
                current = pd.Series(0.0, index=px.columns)
                for t in top3:
                    current.loc[t] = 1.0 / 3
        pos.loc[d] = current

    strat = (pos.shift(1).fillna(0.0) * rets).sum(axis=1)
    bench = {"equal_weight": rets.mean(axis=1)}
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["equal_weight"]))
    return Result(
        meta=META,
        primary_series=mom.mean(axis=1).rename("avg 12M mom"),
        asset_series=px.mean(axis=1),
        strategy_returns=strat,
        benchmark_returns=bench,
        verdict=verdict,
        verdict_why=why,
        notes="long-only top 3 by 12M total return; monthly rebal",
    )
