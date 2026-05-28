# csi300_sma250_timing — 沪深300 250日均线 趋势开关
family: **trend** · literature verdict: **mixed**

### Result: **surprise+**

strat sharpe +0.71 vs bench +0.38 (Δ=+0.33); CAGR Δ=+5.01%; bucket monotonic ok=True

## strategy stats
| metric | value |
|---|---|
| n_days | 5666
| total | 10.5742
| cagr | 0.1151
| sharpe | 0.7129
| maxdd | -0.3638

## benchmark comparison
| benchmark       |   n_days |   total |   cagr |   sharpe |   maxdd |
|:----------------|---------:|--------:|-------:|---------:|--------:|
| csi300_buy_hold |     5666 |  3.1214 | 0.065  |   0.3794 |  -0.723 |
| cash_3m         |     5666 |  0.4815 | 0.0176 |  14.6428 |   0     |

## bucket forward-return table
| bkt   |     20d |     60d |   120d |
|:------|--------:|--------:|-------:|
| q1    |  0.003  |  0.0194 | 0.0467 |
| q2    | -0.0005 |  0.0056 | 0.0319 |
| q3    |  0.0003 | -0.012  | 0.0011 |
| q4    |  0.003  |  0.0233 | 0.0415 |
| q5    |  0.0333 |  0.0916 | 0.1743 |

---
_notes_: bucket monotonicity ρ=+0.30