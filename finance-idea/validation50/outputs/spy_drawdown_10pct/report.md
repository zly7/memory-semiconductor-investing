# spy_drawdown_10pct — SPY 从近 1Y 高点回撤 10% 买入
family: **mean_reversion** · literature verdict: **mixed**

### Result: **null**

strat sharpe +0.65 vs bench +0.73 (Δ=-0.09); CAGR Δ=-3.01%

## strategy stats
| metric | value |
|---|---|
| n_days | 2865
| total | 1.6804
| cagr | 0.0906
| sharpe | 0.6456
| maxdd | -0.2874

## benchmark comparison
| benchmark    |   n_days |   total |   cagr |   sharpe |   maxdd |
|:-------------|---------:|--------:|-------:|---------:|--------:|
| spy_buy_hold |     2865 |  2.6538 | 0.1207 |   0.7319 |  -0.341 |
| bil_cash     |     2865 |  0.0014 | 0.0001 |   0.0199 |  -0.007 |

## bucket forward-return table
|            |    20d |    60d |   120d |   252d |
|:-----------|-------:|-------:|-------:|-------:|
| flag=False | 0.0078 | 0.0233 | 0.0499 | 0.1106 |
| flag=True  | 0.024  | 0.0603 | 0.102  | 0.2225 |

---
_notes_: trigger days: 403 | hold 120d post-trigger