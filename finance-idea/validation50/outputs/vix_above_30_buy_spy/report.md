# vix_above_30_buy_spy — VIX > 30 抄底 SPY
family: **sentiment** · literature verdict: **robust**

### Result: **confirmed**

strat sharpe +0.67 vs bench +0.73 (Δ=-0.06); CAGR Δ=-3.09%

## strategy stats
| metric | value |
|---|---|
| n_days | 2865
| total | 1.6581
| cagr | 0.0898
| sharpe | 0.6747
| maxdd | -0.2874

## benchmark comparison
| benchmark    |   n_days |   total |   cagr |   sharpe |   maxdd |
|:-------------|---------:|--------:|-------:|---------:|--------:|
| spy_buy_hold |     2865 |  2.6538 | 0.1207 |   0.7319 |  -0.341 |
| bil_cash     |     2865 |  0.0014 | 0.0001 |   0.0199 |  -0.007 |

## bucket forward-return table
|            |    20d |    60d |   120d |   252d |
|:-----------|-------:|-------:|-------:|-------:|
| flag=False | 0.0076 | 0.0243 | 0.0518 | 0.1177 |
| flag=True  | 0.0517 | 0.1009 | 0.1539 | 0.2874 |

---
_notes_: in-market days: 933/2865