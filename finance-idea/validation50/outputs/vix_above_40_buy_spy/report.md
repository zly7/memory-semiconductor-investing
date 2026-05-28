# vix_above_40_buy_spy — VIX > 40 强抄底 SPY
family: **sentiment** · literature verdict: **robust**

### Result: **decayed**

strat sharpe +0.52 vs bench +0.73 (Δ=-0.21); CAGR Δ=-6.51%

## strategy stats
| metric | value |
|---|---|
| n_days | 2865
| total | 0.8503
| cagr | 0.0556
| sharpe | 0.5239
| maxdd | -0.3218

## benchmark comparison
| benchmark    |   n_days |   total |   cagr |   sharpe |   maxdd |
|:-------------|---------:|--------:|-------:|---------:|--------:|
| spy_buy_hold |     2865 |  2.6538 | 0.1207 |   0.7319 |  -0.341 |
| bil_cash     |     2865 |  0.0014 | 0.0001 |   0.0199 |  -0.007 |

## bucket forward-return table
|            |    20d |    60d |   120d |   252d |
|:-----------|-------:|-------:|-------:|-------:|
| flag=False | 0.0091 | 0.0262 | 0.0542 | 0.1221 |
| flag=True  | 0.0797 | 0.193  | 0.2879 | 0.4955 |

---
_notes_: trigger days: 40 | in-market days: 533