"""06 — Antonacci GEM (Global Equity Momentum): SPY vs VEU vs AGG, monthly."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import daily_returns, classify_verdict

META = StrategyMeta(
    id="antonacci_gem",
    name_cn="Antonacci GEM 双动量",
    family="trend",
    lit_verdict="robust→decay",
)


@register(META.id)
def compute() -> Result:
    spy = load_price("SPY")
    veu = load_price("VEU")
    agg = load_price("AGG")
    bil = load_price("BIL")
    common = spy.index.intersection(veu.index).intersection(agg.index).intersection(bil.index)
    spy, veu, agg, bil = spy.loc[common], veu.loc[common], agg.loc[common], bil.loc[common]

    # 12-month return ≈ 252 days
    spy12 = spy.pct_change(252)
    veu12 = veu.pct_change(252)
    bil12 = bil.pct_change(252)

    monthly_idx = spy.resample("M").last().index

    # Build daily position by carrying forward monthly decisions
    pos = pd.DataFrame(0.0, index=spy.index, columns=["SPY", "VEU", "AGG"])
    last_choice = "AGG"
    for d in spy.index:
        if d in monthly_idx:
            s12 = spy12.loc[d]
            v12 = veu12.loc[d]
            b12 = bil12.loc[d]
            if pd.isna(s12) or pd.isna(v12) or pd.isna(b12):
                pass
            elif s12 > b12 and s12 >= v12:
                last_choice = "SPY"
            elif v12 > b12:
                last_choice = "VEU"
            else:
                last_choice = "AGG"
        pos.loc[d, last_choice] = 1.0

    rets = pd.DataFrame({
        "SPY": daily_returns(spy), "VEU": daily_returns(veu), "AGG": daily_returns(agg),
    })
    strat = (pos.shift(1).fillna(0.0) * rets).sum(axis=1)
    bench = {"spy_buy_hold": rets["SPY"], "agg_buy_hold": rets["AGG"]}
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["spy_buy_hold"]))
    return Result(
        meta=META,
        primary_series=pos["SPY"].rename("in SPY"),
        asset_series=spy,
        strategy_returns=strat,
        benchmark_returns=bench,
        verdict=verdict,
        verdict_why=why,
        notes="monthly rotation: SPY if 12M>SPY beats VEU & BIL; else VEU; else AGG",
    )
