# connors_rsi2_csi300 — RSI(2) 沪深300
family: **mean_reversion** · literature verdict: **mixed**

### Result: **null**

strat sharpe +0.37 vs bench +0.35 (Δ=+0.02); CAGR Δ=-1.59%; bucket monotonic ok=False

## strategy stats
| metric | value |
|---|---|
| n_days | 5915
| total | 1.6113
| cagr | 0.0417
| sharpe | 0.3721
| maxdd | -0.4929

## benchmark comparison
| benchmark       |   n_days |   total |   cagr |   sharpe |   maxdd |
|:----------------|---------:|--------:|-------:|---------:|--------:|
| csi300_buy_hold |     5915 |  2.7283 | 0.0577 |   0.3511 |  -0.723 |
| cash_3m         |     5915 |  0.5052 | 0.0176 |  14.9031 |   0     |

## bucket forward-return table
| bkt   |      5d |    20d |    60d |
|:------|--------:|-------:|-------:|
| q1    |  0.0038 | 0.007  | 0.0291 |
| q2    |  0.0041 | 0.007  | 0.0288 |
| q3    | -0.002  | 0.0094 | 0.0378 |
| q4    |  0.0018 | 0.0144 | 0.0422 |
| q5    |  0.0049 | 0.0175 | 0.0504 |

---
_notes_: days in market: 1667 | bucket ρ=+0.90