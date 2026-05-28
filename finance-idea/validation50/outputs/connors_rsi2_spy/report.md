# connors_rsi2_spy — Larry Connors RSI(2) SPY
family: **mean_reversion** · literature verdict: **decayed**

### Result: **confirmed**

strat sharpe +0.74 vs bench +0.73 (Δ=+0.01); CAGR Δ=-5.64%; bucket monotonic ok=False

## strategy stats
| metric | value |
|---|---|
| n_days | 2865
| total | 1.0310
| cagr | 0.0643
| sharpe | 0.7385
| maxdd | -0.1812

## benchmark comparison
| benchmark    |   n_days |   total |   cagr |   sharpe |   maxdd |
|:-------------|---------:|--------:|-------:|---------:|--------:|
| spy_buy_hold |     2865 |  2.6538 | 0.1207 |   0.7319 |  -0.341 |
| bil_cash     |     2865 |  0.0014 | 0.0001 |   0.0199 |  -0.007 |

## bucket forward-return table
| bkt   |     5d |    20d |    60d |
|:------|-------:|-------:|-------:|
| q1    | 0.0037 | 0.0112 | 0.0296 |
| q2    | 0.0054 | 0.0206 | 0.0568 |
| q3    | 0.004  | 0.0133 | 0.0476 |
| q4    | 0.0028 | 0.0117 | 0.0361 |
| q5    | 0.0021 | 0.0142 | 0.0338 |

---
_notes_: days in market: 1092 | bucket ρ=+0.00 (expect negative)