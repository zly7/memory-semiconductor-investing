"""14 — 11-sector 1-month reversal: long bottom 3 / short top 3 each month."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import daily_returns, classify_verdict
from .sector_xsmom import SECTORS

META = StrategyMeta(
    id="short_reversal_sectors",
    name_cn="11 行业 1 月反转",
    family="mean_reversion",
    lit_verdict="decayed",
)


@register(META.id)
def compute() -> Result:
    px_dict = {}
    for s in SECTORS:
        try:
            px_dict[s] = load_price(s)
        except FileNotFoundError:
            continue
    common = None
    for s in px_dict.values():
        common = s.index if common is None else common.intersection(s.index)
    px = pd.DataFrame({k: v.loc[common] for k, v in px_dict.items()})
    last_month_ret = px.pct_change(21)
    rets = px.pct_change().fillna(0.0)

    monthly_idx = px.resample("M").last().index
    pos = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    cur = pd.Series(0.0, index=px.columns)
    for d in px.index:
        if d in monthly_idx:
            m = last_month_ret.loc[d].dropna()
            if len(m) >= 6:
                ranked = m.rank(ascending=False)
                cur = pd.Series(0.0, index=px.columns)
                # winners = recent top → SHORT (reversal); losers = bottom → LONG
                top = ranked[ranked <= 3].index
                bot = ranked[ranked > len(m) - 3].index
                for t in top:
                    cur.loc[t] = -1.0 / 3
                for b in bot:
                    cur.loc[b] = 1.0 / 3
        pos.loc[d] = cur

    strat = (pos.shift(1).fillna(0.0) * rets).sum(axis=1)
    bench = {"equal_weight": rets.mean(axis=1)}
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["equal_weight"]))
    return Result(
        meta=META, primary_series=last_month_ret.mean(axis=1).rename("avg 1M ret"),
        asset_series=px.mean(axis=1),
        strategy_returns=strat, benchmark_returns=bench,
        verdict=verdict, verdict_why=why,
        notes="long-short, dollar-neutral; benchmark = equal-weight",
    )
