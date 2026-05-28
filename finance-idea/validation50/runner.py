"""Reusable backtest + reporting framework for the 50-strategy validation.

Each strategy module exposes:

    META = StrategyMeta(id, name_cn, family, lit_verdict, expectation_md)
    def compute(ctx: Context) -> Result: ...

Where Context provides cached loaders and Result is a structured dataclass.

The runner:
    1. Calls compute() for each registered id.
    2. Saves a 4-panel PNG and a per-strategy markdown report.
    3. Aggregates results into a scorecard.
"""
from __future__ import annotations

import json
import pathlib
import sys
import traceback
from dataclasses import asdict, dataclass, field
from typing import Callable, Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "finance-data-api"))

from storage import Storage  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent / "outputs"
OUT.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Loaders (shared across strategies)
# ---------------------------------------------------------------------------
_storage = Storage()


def load_price(key: str, col: str = "close") -> pd.Series:
    df = _storage.load("prices", key)
    if df is None or df.empty:
        raise FileNotFoundError(f"prices/{key}")
    if col not in df.columns:
        for fb in ("close", "adj_close", "latest"):
            if fb in df.columns:
                col = fb; break
    return df[col].dropna().astype(float)


def load_nav(key: str) -> pd.Series:
    df = _storage.load("nav", key)
    if df is None or df.empty:
        raise FileNotFoundError(f"nav/{key}")
    return df["nav"].dropna().astype(float)


def load_macro(key: str) -> pd.DataFrame:
    df = _storage.load("macro", key)
    if df is None or df.empty:
        raise FileNotFoundError(f"macro/{key}")
    return df


def load_macro_value(key: str) -> pd.Series:
    df = load_macro(key)
    col = "value" if "value" in df.columns else df.select_dtypes(include="number").columns[0]
    return df[col].dropna().astype(float)


# ---------------------------------------------------------------------------
# Stats helpers
# ---------------------------------------------------------------------------
def equity(daily_ret: pd.Series) -> pd.Series:
    return (1.0 + daily_ret.fillna(0)).cumprod()


def stats(daily_ret: pd.Series) -> dict:
    daily_ret = daily_ret.dropna()
    if daily_ret.empty:
        return dict(cagr=None, sharpe=None, maxdd=None, total=None, n_days=0)
    eq = equity(daily_ret)
    years = len(daily_ret) / 252.0
    cagr = eq.iloc[-1] ** (1 / years) - 1 if years > 0 else None
    sharpe = (daily_ret.mean() / daily_ret.std() * np.sqrt(252)
              if daily_ret.std() > 0 else None)
    dd = float((eq / eq.cummax() - 1).min())
    return dict(
        n_days=int(len(daily_ret)),
        total=float(eq.iloc[-1] - 1),
        cagr=None if cagr is None else float(cagr),
        sharpe=None if sharpe is None else float(sharpe),
        maxdd=dd,
    )


def dca_series(price: pd.Series, contribution_freq: str = "ME") -> pd.Series:
    """Simulate equal-dollar DCA. Returns equity curve (cash $1/period)."""
    price = price.dropna()
    contrib_dates = price.resample(contribution_freq).first().dropna().index
    units = 0.0
    eq = []
    for d, p in price.items():
        if d in contrib_dates:
            units += 1.0 / p
        eq.append(units * p)
    s = pd.Series(eq, index=price.index, name="dca_equity")
    return s


def cash_growth(tbill_yield: pd.Series, start_value: float = 1.0) -> pd.Series:
    """Equity curve of cash earning a (annualized) T-bill yield series, daily."""
    y = tbill_yield.reindex(tbill_yield.index.union(pd.date_range(
        tbill_yield.index.min(), pd.Timestamp.today(), freq="B"))).ffill()
    daily = (y / 100.0) / 252.0
    return start_value * (1.0 + daily.fillna(0)).cumprod()


# ---------------------------------------------------------------------------
# Result schema
# ---------------------------------------------------------------------------
@dataclass
class StrategyMeta:
    id: str
    name_cn: str
    family: str
    lit_verdict: str
    expectation_md: str = ""


@dataclass
class Result:
    meta: StrategyMeta
    primary_series: pd.Series          # signal value time series
    asset_series: Optional[pd.Series] = None
    strategy_returns: Optional[pd.Series] = None
    benchmark_returns: dict = field(default_factory=dict)  # name → daily ret series
    buckets: Optional[pd.DataFrame] = None
    extra_chart: Optional[Callable[[plt.Axes], None]] = None
    verdict: str = "tbd"               # confirmed | decayed | surprise+ | surprise- | null
    verdict_why: str = ""
    notes: str = ""


# ---------------------------------------------------------------------------
# Plot helper — 4-panel PNG per strategy
# ---------------------------------------------------------------------------
def plot_strategy(result: Result, path: pathlib.Path) -> None:
    fig = plt.figure(figsize=(13, 9))
    gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.3)

    # Panel 1 — signal + asset overlay
    ax1 = fig.add_subplot(gs[0, 0])
    s = result.primary_series.dropna()
    if not s.empty:
        ax1.plot(s.index, s.values, color="tab:red", lw=0.8, label="signal")
    if result.asset_series is not None and not result.asset_series.empty:
        ax1b = ax1.twinx()
        ax1b.plot(result.asset_series.index, result.asset_series.values,
                  color="tab:gray", lw=0.8, alpha=0.7, label="asset")
        ax1b.set_ylabel("asset")
    ax1.set_title(f"signal ({result.meta.name_cn})")
    ax1.grid(alpha=0.3)
    ax1.set_ylabel("signal")

    # Panel 2 — equity curves
    ax2 = fig.add_subplot(gs[0, 1])
    if result.strategy_returns is not None:
        eq = equity(result.strategy_returns)
        ax2.plot(eq.index, eq.values, label="strategy", color="tab:red", lw=1.2)
    for name, br in (result.benchmark_returns or {}).items():
        if br is None or br.empty:
            continue
        eqb = equity(br)
        ax2.plot(eqb.index, eqb.values, label=name, lw=0.9, alpha=0.85)
    ax2.set_title("net asset value (start = 1)")
    ax2.legend(fontsize=8)
    ax2.grid(alpha=0.3)
    ax2.set_yscale("log")

    # Panel 3 — bucket / extra
    ax3 = fig.add_subplot(gs[1, 0])
    if result.buckets is not None and not result.buckets.empty:
        result.buckets.plot.bar(ax=ax3)
        ax3.axhline(0, color="black", lw=0.5)
        ax3.set_title("forward return by signal bucket")
        ax3.legend(fontsize=8)
    elif result.extra_chart is not None:
        result.extra_chart(ax3)
    else:
        ax3.text(0.5, 0.5, "(no bucket chart)", ha="center", va="center")
        ax3.axis("off")
    ax3.grid(alpha=0.3)

    # Panel 4 — strategy returns drawdown
    ax4 = fig.add_subplot(gs[1, 1])
    if result.strategy_returns is not None:
        eq = equity(result.strategy_returns)
        dd = eq / eq.cummax() - 1
        ax4.fill_between(dd.index, dd.values, 0, color="tab:red", alpha=0.4)
        ax4.set_title("strategy drawdown")
    else:
        ax4.text(0.5, 0.5, "(no strategy returns)", ha="center", va="center")
        ax4.axis("off")
    ax4.grid(alpha=0.3)

    fig.suptitle(f"{result.meta.id} — {result.meta.name_cn}  [{result.meta.family}]",
                 fontsize=12, fontweight="bold")
    plt.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Per-strategy markdown report
# ---------------------------------------------------------------------------
def write_report(result: Result, path: pathlib.Path) -> None:
    md = []
    md.append(f"# {result.meta.id} — {result.meta.name_cn}")
    md.append(f"family: **{result.meta.family}** · literature verdict: **{result.meta.lit_verdict}**")
    md.append("")
    md.append(f"### Result: **{result.verdict}**")
    md.append("")
    md.append(result.verdict_why)
    md.append("")
    if result.strategy_returns is not None:
        st = stats(result.strategy_returns)
        md.append("## strategy stats")
        md.append("| metric | value |")
        md.append("|---|---|")
        for k, v in st.items():
            md.append(f"| {k} | {v:.4f}" if isinstance(v, float) else f"| {k} | {v}")
        md.append("")
    if result.benchmark_returns:
        md.append("## benchmark comparison")
        rows = []
        for name, br in result.benchmark_returns.items():
            rows.append({"benchmark": name, **stats(br)})
        df = pd.DataFrame(rows).round(4)
        md.append(df.to_markdown(index=False))
        md.append("")
    if result.buckets is not None and not result.buckets.empty:
        md.append("## bucket forward-return table")
        md.append(result.buckets.round(4).to_markdown())
        md.append("")
    md.append("---")
    md.append(f"_notes_: {result.notes}")
    path.write_text("\n".join(md), encoding="utf-8")


# ---------------------------------------------------------------------------
# Registry + run-all driver
# ---------------------------------------------------------------------------
REGISTRY: dict[str, Callable[[], Result]] = {}


def register(strategy_id: str):
    """Decorator: `@register("spy_sma200_timing")` on compute()."""
    def deco(fn):
        REGISTRY[strategy_id] = fn
        return fn
    return deco


def run_one(strategy_id: str, save: bool = True) -> dict:
    fn = REGISTRY[strategy_id]
    out_dir = OUT / strategy_id
    out_dir.mkdir(exist_ok=True)
    try:
        result: Result = fn()
        if save:
            plot_strategy(result, out_dir / "chart.png")
            write_report(result, out_dir / "report.md")
        st = stats(result.strategy_returns) if result.strategy_returns is not None else {}
        bench = {n: stats(br) for n, br in (result.benchmark_returns or {}).items()}
        return {
            "id": strategy_id,
            "name_cn": result.meta.name_cn,
            "family": result.meta.family,
            "lit_verdict": result.meta.lit_verdict,
            "our_verdict": result.verdict,
            "verdict_why": result.verdict_why,
            "stats": st,
            "benchmarks": bench,
            "status": "ok",
        }
    except Exception as e:  # noqa: BLE001
        traceback.print_exc()
        return {"id": strategy_id, "status": "error", "error": str(e)}


def run_all(ids: Optional[list[str]] = None) -> list[dict]:
    if ids is None:
        ids = list(REGISTRY.keys())
    rows = []
    for sid in ids:
        print(f"[run] {sid}")
        rows.append(run_one(sid))
    return rows


def write_scorecard(rows: list[dict]) -> None:
    df = pd.DataFrame(rows)
    (OUT / "scorecard.json").write_text(
        df.to_json(orient="records", indent=2, force_ascii=False),
        encoding="utf-8",
    )
    by_verdict = df.groupby("our_verdict").size() if "our_verdict" in df else None
    md = ["# Scorecard", ""]
    if by_verdict is not None:
        md.append("## Verdict tally")
        md.append("| our_verdict | count |")
        md.append("|---|---|")
        for v, c in by_verdict.items():
            md.append(f"| {v} | {c} |")
        md.append("")

    # --- Biggest surprises (vs primary benchmark) ---
    def _bench_sharpe(r):
        bs = r.get("benchmarks") or {}
        for k in ("spy_buy_hold", "equal_weight", "csi300_buy_hold",
                  "eq_50_50", "eq_spy_eem", "always_dca"):
            if k in bs:
                return bs[k].get("sharpe") or 0.0
        # fallback: first benchmark
        return next(iter(bs.values()), {}).get("sharpe") or 0.0

    scored = []
    for r in rows:
        if r.get("status") != "ok":
            continue
        ss = (r.get("stats") or {}).get("sharpe") or 0.0
        bs = _bench_sharpe(r)
        scored.append((r, ss - bs))
    scored.sort(key=lambda t: t[1], reverse=True)
    pos_surprises = [t for t in scored if t[1] > 0.0][:5]
    neg_surprises = sorted(scored, key=lambda t: t[1])[:5]

    md.append("## Top 5 positive surprises (highest Sharpe edge over benchmark)")
    md.append("| id | family | lit | ours | sharpe gap | strat CAGR |")
    md.append("|---|---|---|---|---|---|")
    for r, gap in pos_surprises:
        cagr = (r.get("stats") or {}).get("cagr") or 0.0
        md.append(f"| `{r['id']}` | {r['family']} | {r['lit_verdict']} | **{r['our_verdict']}** "
                  f"| +{gap:.2f} | {cagr:.2%} |")
    md.append("")
    md.append("## Top 5 negative surprises (worst Sharpe gap vs benchmark)")
    md.append("| id | family | lit | ours | sharpe gap | strat CAGR |")
    md.append("|---|---|---|---|---|---|")
    for r, gap in neg_surprises:
        cagr = (r.get("stats") or {}).get("cagr") or 0.0
        md.append(f"| `{r['id']}` | {r['family']} | {r['lit_verdict']} | **{r['our_verdict']}** "
                  f"| {gap:+.2f} | {cagr:.2%} |")
    md.append("")

    md.append("## Per-strategy (sorted by family)")
    md.append("| id | family | name_cn | lit | ours | total | sharpe | maxdd | why |")
    md.append("|---|---|---|---|---|---|---|---|---|")
    rows_sorted = sorted(rows, key=lambda r: (r.get("family") or "", r.get("id") or ""))
    for r in rows_sorted:
        if r.get("status") != "ok":
            md.append(f"| {r['id']} | err | — | — | err | — | — | — | {r.get('error','')} |")
            continue
        st = r.get("stats", {})
        md.append(
            f"| `{r['id']}` | {r['family']} | {r['name_cn']} | {r['lit_verdict']} "
            f"| **{r['our_verdict']}** | "
            f"{(st.get('total') or 0):.2%} | "
            f"{(st.get('sharpe') or 0):.2f} | "
            f"{(st.get('maxdd') or 0):.2%} | "
            f"{r['verdict_why'][:100]} |"
        )
    (OUT / "scorecard.md").write_text("\n".join(md), encoding="utf-8")


def main():
    # Auto-discover strategy modules
    import importlib
    strat_dir = pathlib.Path(__file__).resolve().parent / "strategies"
    sys.path.insert(0, str(strat_dir.parent))
    for p in sorted(strat_dir.glob("*.py")):
        if p.name.startswith("_"):
            continue
        importlib.import_module(f"strategies.{p.stem}")
    rows = run_all()
    write_scorecard(rows)
    print(f"\nDone. Wrote {OUT/'scorecard.md'} and {OUT/'scorecard.json'}")


if __name__ == "__main__":
    # When invoked as `python runner.py`, this module is `__main__`. Strategies
    # do `from runner import ...`, which would otherwise load a SECOND copy of
    # this file and register on a different REGISTRY. Alias both names to the
    # same module so the registry is shared.
    sys.modules["runner"] = sys.modules["__main__"]
    main()
