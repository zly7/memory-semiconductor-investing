# dxy_6m_em_tilt — DXY 6 月跌幅 → EEM 加仓
family: **macro** · literature verdict: **robust**

### Result: **confirmed**

strat sharpe +0.57 vs bench +0.56 (Δ=+0.01); CAGR Δ=+0.36%; bucket monotonic ok=True

## strategy stats
| metric | value |
|---|---|
| n_days | 2863
| total | 1.7108
| cagr | 0.0917
| sharpe | 0.5734
| maxdd | -0.3322

## benchmark comparison
| benchmark    |   n_days |   total |   cagr |   sharpe |   maxdd |
|:-------------|---------:|--------:|-------:|---------:|--------:|
| spy_buy_hold |     2863 |  2.6538 | 0.1208 |   0.7323 | -0.341  |
| eem_buy_hold |     2863 |  0.7643 | 0.0512 |   0.3448 | -0.4146 |
| eq_spy_eem   |     2863 |  1.6108 | 0.0881 |   0.5596 | -0.3322 |

## bucket forward-return table
| bkt   |     60d |   120d |   252d |
|:------|--------:|-------:|-------:|
| q1    |  0.0586 | 0.0819 | 0.0425 |
| q2    |  0.0016 | 0.0133 | 0.0604 |
| q3    |  0.0077 | 0.0323 | 0.1037 |
| q4    |  0.019  | 0.0158 | 0.0626 |
| q5    | -0.0069 | 0.0148 | 0.0679 |

---
_notes_: bucket ρ=-0.40 (expect negative: weak USD → strong EM)