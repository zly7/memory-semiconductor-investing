# iwm_spy_zscore — IWM/SPY 相对强度 z
family: **cross_asset** · literature verdict: **mixed**

### Result: **null**

strat sharpe +0.59 vs bench +0.60 (Δ=-0.01); CAGR Δ=+0.07%; bucket monotonic ok=True

## strategy stats
| metric | value |
|---|---|
| n_days | 2865
| total | 2.0651
| cagr | 0.1035
| sharpe | 0.5889
| maxdd | -0.4009

## benchmark comparison
| benchmark    |   n_days |   total |   cagr |   sharpe |   maxdd |
|:-------------|---------:|--------:|-------:|---------:|--------:|
| spy_buy_hold |     2865 |  2.6538 | 0.1207 |   0.7319 | -0.341  |
| iwm_buy_hold |     2865 |  1.4427 | 0.0817 |   0.4623 | -0.4226 |
| eq_50_50     |     2865 |  2.0433 | 0.1028 |   0.6015 | -0.3743 |

## bucket forward-return table
| bkt   |     20d |     60d |    120d |
|:------|--------:|--------:|--------:|
| q1    |  0.0018 |  0.0024 | -0.0049 |
| q2    | -0.0048 | -0.016  | -0.014  |
| q3    | -0.0037 | -0.0113 | -0.0069 |
| q4    | -0.002  | -0      | -0.011  |
| q5    | -0.005  | -0.0173 | -0.0545 |

---
_notes_: 