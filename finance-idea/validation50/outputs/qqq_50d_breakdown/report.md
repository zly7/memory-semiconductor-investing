# qqq_50d_breakdown — QQQ 跌破 50日均线 3% 反弹
family: **mean_reversion** · literature verdict: **mixed**

### Result: **null**

strat sharpe +0.77 vs bench +0.90 (Δ=-0.13); CAGR Δ=-6.11%

## strategy stats
| metric | value |
|---|---|
| n_days | 2865
| total | 2.8933
| cagr | 0.1270
| sharpe | 0.7698
| maxdd | -0.2737

## benchmark comparison
| benchmark    |   n_days |   total |   cagr |   sharpe |   maxdd |
|:-------------|---------:|--------:|-------:|---------:|--------:|
| qqq_buy_hold |     2865 |  6.0942 | 0.1881 |   0.8978 | -0.3562 |
| bil_cash     |     2865 |  0.0014 | 0.0001 |   0.0199 | -0.007  |

## bucket forward-return table
|            |     5d |    20d |    60d |
|:-----------|-------:|-------:|-------:|
| flag=False | 0.0036 | 0.0131 | 0.0384 |
| flag=True  | 0.005  | 0.0272 | 0.071  |

---
_notes_: trigger days: 408 | hold 20d post-trigger