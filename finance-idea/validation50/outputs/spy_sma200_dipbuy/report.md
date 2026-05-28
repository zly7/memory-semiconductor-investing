# spy_sma200_dipbuy — SPY 200日均线下方持续买入
family: **trend** · literature verdict: **decayed**

### Result: **confirmed**

strat sharpe +0.42 vs bench +0.78 (Δ=-0.37); CAGR Δ=-8.31%; bucket monotonic ok=False

## strategy stats
| metric | value |
|---|---|
| n_days | 2666
| total | 0.6558
| cagr | 0.0488
| sharpe | 0.4178
| maxdd | -0.2629

## benchmark comparison
| benchmark    |   n_days |   total |   cagr |   sharpe |   maxdd |
|:-------------|---------:|--------:|-------:|---------:|--------:|
| spy_buy_hold |     2666 |  2.7094 | 0.1319 |   0.7832 |  -0.341 |
| bil_cash     |     2666 |  0.0025 | 0.0002 |   0.0334 |  -0.007 |

## bucket forward-return table
| bkt   |    20d |    60d |   120d |
|:------|-------:|-------:|-------:|
| q1    | 0.0179 | 0.046  | 0.087  |
| q2    | 0.0125 | 0.0388 | 0.0613 |
| q3    | 0.0103 | 0.0312 | 0.0498 |
| q4    | 0.0081 | 0.0111 | 0.0482 |
| q5    | 0.0042 | 0.0268 | 0.0712 |

---
_notes_: invert of 01 — buy ONLY when in downtrend