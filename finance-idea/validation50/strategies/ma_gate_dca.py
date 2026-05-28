"""10 — 200d SMA gate for DCA: monthly contribution only when SPY < SMA200."""
import pandas as pd
from runner import StrategyMeta, Result, register, load_price, stats
from ._helpers import daily_returns, sma, cash_ret_from_bil, classify_verdict

META = StrategyMeta(
    id="ma_gate_dca",
    name_cn="200日 SMA 门控定投",
    family="trend",
    lit_verdict="decayed",
)


def _dca_eq(price: pd.Series, gate: pd.Series) -> pd.Series:
    """Each month-end, if gate is True, contribute $1 into the asset. Equity tracks total value."""
    contrib_dates = price.resample("M").last().index
    units = 0.0
    cash = 0.0
    eq = []
    for d, p in price.items():
        if d in contrib_dates:
            if bool(gate.loc[d]) if d in gate.index else False:
                units += 1.0 / p
            else:
                cash += 1.0
        eq.append(units * p + cash)
    return pd.Series(eq, index=price.index)


@register(META.id)
def compute() -> Result:
    spy = load_price("SPY")
    sma200 = sma(spy, 200)
    gate = (spy < sma200).fillna(False)

    eq_gated = _dca_eq(spy, gate)
    eq_always = _dca_eq(spy, pd.Series(True, index=spy.index))

    # Trim to where equity > 0; convert to daily returns, neutralizing
    # contribution-day inflows so Sharpe reflects investment performance only.
    def _eq_to_strat_ret(eq: pd.Series, p: pd.Series, contrib_dates):
        eq = eq[eq > 0]
        units = (eq / p.loc[eq.index]).ffill()
        # Strategy "return" = SPY return weighted by units$ / total wealth
        spy_ret = p.pct_change().fillna(0.0)
        weight = (units * p) / eq.replace(0, pd.NA)
        weight = weight.fillna(0.0).clip(0, 1)
        return (weight.shift(1).fillna(0.0) * spy_ret.loc[eq.index]).astype(float)

    contrib_dates = spy.resample("M").last().index
    strat = _eq_to_strat_ret(eq_gated, spy, contrib_dates)
    bench_dca = _eq_to_strat_ret(eq_always, spy, contrib_dates)
    bench_spy = daily_returns(spy)

    bench = {"always_dca": bench_dca, "spy_buy_hold": bench_spy}
    verdict, why = classify_verdict(META.lit_verdict,
                                    stats(strat), stats(bench["always_dca"]))
    return Result(
        meta=META,
        primary_series=(spy / sma200 - 1.0).dropna(),
        asset_series=spy,
        strategy_returns=strat,
        benchmark_returns=bench,
        verdict=verdict,
        verdict_why=why,
        notes="gate compares to always-on DCA; both contribute $1/month",
    )
