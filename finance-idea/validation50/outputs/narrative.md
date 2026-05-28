# 50 Strategy Validation — Surprise Narrative

_Run date: 2026-05-27 · 50/50 strategies executed · 5 skipped (data unavailable)_

The cleanly-implementable rules from 4 deep-research reports were forced through
one unified backtest framework over the 2015–2026 window (US strategies use
SPY+BIL since 2015; CN strategies use CSI300 since 2002). The runner records
strategy daily P&L, picks a reasonable benchmark (most often `spy_buy_hold` or
`equal_weight`), and writes `our_verdict ∈ {confirmed, decayed, surprise+,
surprise-, null, skipped}` based on Sharpe gap vs benchmark.

## Headline verdict tally

| our_verdict | count |
|---|---|
| confirmed   | 13 |
| decayed     | 11 |
| null        | 16 |
| surprise+   |  3 |
| surprise-   |  2 |
| skipped     |  5 |

Of the 45 runnable strategies, **about 27% (13/45) cleanly confirmed the
literature claim, 24% (11/45) decayed, 11% (5/45) produced an unambiguous
surprise (3 better, 2 worse), and the remaining 36% (16/45) landed in a "null"
band where strat ≈ bench within 0.2 Sharpe.** The robust-claim camp held up
unevenly: factor and allocation portfolios mostly survived, but trend-following
multi-asset rotations (Faber GTAA5, All Weather) decayed noticeably during this
era of US-led growth dominance.

---

## Five biggest positive surprises

### 1. `csi300_sma250_timing` — surprise+, Sharpe Δ = +0.33

The plain 250-day SMA on/off filter on CSI300 turns a **+5.0 pp/yr CAGR over
buy-and-hold** with a Sharpe of 0.71 vs CSI300's 0.38, and total return 1057%
vs buy-and-hold ~315%. The bucket forward-return table is monotonic: deep
deviations below the SMA precede the worst 60d returns, deep deviations above
it precede the best.

**Why this beats the US analogue**: A-shares spent multi-year stretches in
declining trends (2015–2018, 2021–2024). Staying flat through them is more
valuable than for SPY, where avoided drawdowns get partly returned during the
long bull legs. The "lit_verdict=mixed" claim was too pessimistic — for A-shares
specifically this is the closest thing to a free lunch in the deck.

### 2. `northbound_flow` — surprise+, Sharpe Δ = +0.27

Going long CSI300 only when the 20-day cumulative northbound net inflow is
positive cleanly beats buy-and-hold: Sharpe 0.40 vs 0.14, +5.3 pp/yr. The
bucket table is monotonic (positive ρ), so the signal has real directional
content. This contradicts the deep-research framing that *high* northbound
flow is contrarian-bearish — at the **20-day** horizon the trend-following
side dominates the contrarian-extreme side.

### 3. `cn_spring_festival` — surprise+, Sharpe Δ = +0.24

10 trading days before to 5 after the Lunar New Year, holding CSI300 yields a
Sharpe of 0.59 vs the full-period 0.35 — and crucially only ~15 days/year in
market means a max drawdown of just -12% vs CSI300's -45%. Small absolute
returns but strong risk-adjusted edge.

### 4. `tsmom_proxy` — confirmed (Sharpe Δ = +0.07) but worth highlighting

Long-only TSMOM across 6 ETFs delivers Sharpe 0.80 vs SPY 0.73 **and** ~12%
max drawdown vs SPY's 34%. The "robust→decay" warning didn't hold up here
because the 2018, 2020, and 2022 drawdowns were filtered out cleanly. Best
risk-adjusted return of any active strategy in the 50.

### 5. `pf_permanent` — confirmed, Sharpe Δ = +0.07

Harry Browne's 1981 25/25/25/25 (SPY/TLT/BIL/GLD) gives Sharpe 0.81 — actually
the highest of all 50 strategies, with -17.6% max DD vs SPY -34%. Forty-year-old
allocation, no fitting, beats every "smart" portfolio in this comparison.

---

## Two cleanest negative surprises

### 1. `sell_in_may` — surprise-, Sharpe Δ = -0.31

Holding SPY only Nov 1 → Apr 30 (winter window) underperformed SPY buy-and-hold
by ~7 pp/yr CAGR with Sharpe 0.42 vs 0.73 in 2015–2026. The summer months we
"avoided" (May–Oct) contained substantial bull-market returns — sitting in BIL
during them was a huge drag. This is the strongest individual rebuttal to a
classic "robust seasonal" claim in the deck.

### 2. `santa_rally` — surprise-, Sharpe Δ = -0.73

Holding SPY only for the canonical Santa window (last 5 trading days of Dec +
first 2 of Jan) basically produced zero return: total -0.3% across ~12 years
of triggers, Sharpe ≈ 0.00. The window is too narrow to compound and the
edge has clearly priced in — multiple years had **negative** returns during the
window.

---

## Notable other patterns

- **Faber GTAA 5 decayed, but trend-on-single-asset (SPY SMA200) survived.**
  The multi-asset rotation across SPY/EFA/IEF/VNQ/DBC got hurt by structurally
  weak non-US assets (EFA, DBC, VNQ) during 2015–2024; the equity component on
  its own (SMA200 on SPY) still confirms.
- **Sector cross-sectional momentum (`sector_xsmom`) clearly decayed** —
  Sharpe 0.13 vs equal-weight 0.63. The 11-sector breadth is too narrow for
  long-short to extract a signal after costs/turnover.
- **Reversal (`short_reversal_sectors`) "confirmed" as decayed** — it was
  expected to fail and it did, hard: -50% total, Sharpe -0.49. Useful negative
  evidence: the 1-month sector reversal trade is dead.
- **Factor ETFs split the difference.** USMV (lowvol) decayed mildly
  (Sharpe 0.60 vs 0.73 — beta cost dominated); QUAL confirmed (Sharpe 0.70).
- **All Weather (Dalio) decayed** — Sharpe 0.50 vs SPY 0.73. In a regime where
  TLT had its worst 5-year stretch in 40 years, bond-heavy allocation paid the
  bill. The "robust→decay" expectation was correct.
- **Macro yield-curve and HY-OAS thresholds (`yc_inversion_defensive`,
  `hy_oas_threshold`, `nfci_positive_defensive`) all landed in the "null /
  decayed" band.** Defensive de-risking based on these triggers cost more in
  bull-market opportunity than it saved in drawdown protection within the
  2015–2026 window.

---

## Caveats

1. **Window is short.** 2015–2026 is one regime (post-GFC, mostly US-led
   equity bull). Claims like "robust" in the deep-research reports often
   reference longer panels (1928–2020). A `surprise-` here usually means
   "didn't work in this decade," not "doesn't work at all."
2. **CSI300 strategies use FRED DGS3MO as a cash proxy.** A proper CN money-
   market rate would shift cash arms by ~50–100 bp.
3. **5 strategies are skipped**: `aaii_bearish_60`, `ah_premium_reversion`,
   `cape_top_decile`, `prefomc_drift`, `put_call_extreme`. These need manual
   CSV drops or fixes to `data_acq.py` — once the data is in `data/macro/`,
   the strategy modules already implement the rules and will start producing
   verdicts on the next run.
4. **The classifier is heuristic.** "Null" means Sharpe gap is within ±0.2;
   raise/lower the band to taste in [`_helpers.classify_verdict`](../strategies/_helpers.py).

---

## What to look at next

- For each `surprise+` row, check whether the edge is concentrated in one
  drawdown (e.g. CSI300 trend-filter saved the 2015 crash → still useful) or
  is spread across many regimes.
- The "null" cohort is the most interesting batch for follow-up — many have
  monotonic bucket tables (`bucket_monotonicity > 0`) yet didn't produce
  cleaner P&L. That means the signal has directional content but the rule
  built on it (binary threshold, etc.) didn't extract it.
- All 50 per-strategy reports + 4-panel PNGs live in `outputs/<id>/`.
