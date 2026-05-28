# yc_resteepen_buy — 10Y-3M 再陡峭化买入
family: **macro** · literature verdict: **mixed**

### Result: **decayed**

strat sharpe +0.50 vs bench +0.73 (Δ=-0.23); CAGR Δ=-6.17%

## strategy stats
| metric | value |
|---|---|
| n_days | 2865
| total | 0.9183
| cagr | 0.0590
| sharpe | 0.4982
| maxdd | -0.3410

## benchmark comparison
| benchmark    |   n_days |   total |   cagr |   sharpe |   maxdd |
|:-------------|---------:|--------:|-------:|---------:|--------:|
| spy_buy_hold |     2865 |  2.6538 | 0.1207 |   0.7319 |  -0.341 |
| bil_cash     |     2865 |  0.0014 | 0.0001 |   0.0199 |  -0.007 |

## bucket forward-return table
|            |    60d |   120d |   252d |
|:-----------|-------:|-------:|-------:|
| flag=False | 0.0285 | 0.0573 | 0.1278 |
| flag=True  | 0.0387 | 0.0862 | 0.1491 |

---
_notes_: resteepen events: 21 | in-market days: 1098