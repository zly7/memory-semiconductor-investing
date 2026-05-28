# bollinger_lower_spy — SPY 布林下轨反弹
family: **mean_reversion** · literature verdict: **mixed**

### Result: **decayed**

strat sharpe +0.49 vs bench +0.73 (Δ=-0.24); CAGR Δ=-6.51%

## strategy stats
| metric | value |
|---|---|
| n_days | 2865
| total | 0.8497
| cagr | 0.0556
| sharpe | 0.4877
| maxdd | -0.2978

## benchmark comparison
| benchmark    |   n_days |   total |   cagr |   sharpe |   maxdd |
|:-------------|---------:|--------:|-------:|---------:|--------:|
| spy_buy_hold |     2865 |  2.6538 | 0.1207 |   0.7319 |  -0.341 |
| bil_cash     |     2865 |  0.0014 | 0.0001 |   0.0199 |  -0.007 |

## bucket forward-return table
|            |     5d |    20d |    60d |
|:-----------|-------:|-------:|-------:|
| flag=False | 0.0022 | 0.0096 | 0.0272 |
| flag=True  | 0.0091 | 0.0198 | 0.0562 |

---
_notes_: in-market days: 523 | bands 20d ±2σ