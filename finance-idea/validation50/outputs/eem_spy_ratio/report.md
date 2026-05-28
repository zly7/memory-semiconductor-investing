# eem_spy_ratio — EEM/SPY 相对强度 z
family: **cross_asset** · literature verdict: **mixed**

### Result: **null**

strat sharpe +0.56 vs bench +0.56 (Δ=-0.00); CAGR Δ=+0.24%; bucket monotonic ok=True

## strategy stats
| metric | value |
|---|---|
| n_days | 2865
| total | 1.6778
| cagr | 0.0905
| sharpe | 0.5564
| maxdd | -0.3259

## benchmark comparison
| benchmark    |   n_days |   total |   cagr |   sharpe |   maxdd |
|:-------------|---------:|--------:|-------:|---------:|--------:|
| spy_buy_hold |     2865 |  2.6538 | 0.1207 |   0.7319 | -0.341  |
| eem_buy_hold |     2865 |  0.7643 | 0.0512 |   0.3446 | -0.4146 |
| eq_50_50     |     2865 |  1.6107 | 0.0881 |   0.5593 | -0.3322 |

## bucket forward-return table
| bkt   |     20d |     60d |    120d |
|:------|--------:|--------:|--------:|
| q1    | -0.0021 |  0.0026 | -0.0104 |
| q2    | -0.0039 | -0.0222 | -0.0394 |
| q3    | -0.013  | -0.0343 | -0.0413 |
| q4    | -0.0015 | -0.0046 | -0.0229 |
| q5    | -0.006  | -0.0214 | -0.0424 |

---
_notes_: 