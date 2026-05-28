# spy_50d_breakdown — SPY 跌破 50日 3% 反弹
family: **mean_reversion** · literature verdict: **mixed**

### Result: **null**

strat sharpe +0.58 vs bench +0.73 (Δ=-0.15); CAGR Δ=-4.65%

## strategy stats
| metric | value |
|---|---|
| n_days | 2865
| total | 1.2557
| cagr | 0.0742
| sharpe | 0.5784
| maxdd | -0.2946

## benchmark comparison
| benchmark    |   n_days |   total |   cagr |   sharpe |   maxdd |
|:-------------|---------:|--------:|-------:|---------:|--------:|
| spy_buy_hold |     2865 |  2.6538 | 0.1207 |   0.7319 |  -0.341 |
| bil_cash     |     2865 |  0.0014 | 0.0001 |   0.0199 |  -0.007 |

## bucket forward-return table
|            |     5d |    20d |    60d |
|:-----------|-------:|-------:|-------:|
| flag=False | 0.0022 | 0.0082 | 0.0237 |
| flag=True  | 0.0048 | 0.0245 | 0.0669 |

---
_notes_: trigger days: 333 | hold 20d post-trigger