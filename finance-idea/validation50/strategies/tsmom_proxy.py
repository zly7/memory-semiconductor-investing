"""07 — Time-series momentum across 6 ETFs (long if 12M ret > 0, else cash)."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import daily_returns, cash_ret_from_bil, classify_verdict

META = StrategyMeta(
    id="tsmom_proxy",
    name_cn="多资产时间序列动量（ETF代理）",
    family="trend",
    lit_verdict="robust→decay",
)

UNIVERSE = ["SPY", "EFA", "EEM", "AGG", "GLD", "DBC"]


@register(META.id)
def compute() -> Result:
    bil = load_price("BIL")
    prices = {k: load_price(k) for k in UNIVERSE}
    common = bil.index
    for s in prices.values():
        common = common.intersection(s.index)
    px = pd.DataFrame({k: v.loc[common] for k, v in prices.items()})
    bil = bil.loc[common]
    rets = px.pct_change().fillna(0.0)
    cash = bil.pct_change().fillna(0.0)

    # 12M return > 0 → long, else cash; 1/N weight per asset; monthly rebal
    mom = px.pct_change(252)
    long_flag = (mom > 0).astype(float)
    monthly_idx = px.resample("M").last().index
    long_at_month = long_flag.loc[long_flag.index.intersection(monthly_idx)]
    daily_pos = long_flag.reindex(rets.index).ffill().fillna(0.0)

    w = daily_pos / len(UNIVERSE)
    cash_w = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    asset_pnl = (w.shift(1).fillna(0.0) * rets).sum(axis=1)
    cash_pnl = cash_w.shift(1).fillna(0.0) * cash
    strat = asset_pnl + cash_pnl

    bench = {"spy_buy_hold": rets["SPY"], "equal_weight": rets.mean(axis=1)}
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META,
        primary_series=daily_pos.sum(axis=1).rename("# assets long"),
        asset_series=px["SPY"],
        strategy_returns=strat,
        benchmark_returns=bench,
        verdict=verdict,
        verdict_why=why,
        notes="long-only TSMOM across 6 ETFs",
    )
