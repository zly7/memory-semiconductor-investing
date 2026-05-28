# antonacci_gem — Antonacci GEM 双动量
family: **trend** · literature verdict: **robust→decay**

### Result: **confirmed**

strat sharpe +0.63 vs bench +0.73 (Δ=-0.10); CAGR Δ=-3.28%

## strategy stats
| metric | value |
|---|---|
| n_days | 2865
| total | 1.6078
| cagr | 0.0880
| sharpe | 0.6291
| maxdd | -0.3410

## benchmark comparison
| benchmark    |   n_days |   total |    cagr |   sharpe |   maxdd |
|:-------------|---------:|--------:|--------:|---------:|--------:|
| spy_buy_hold |     2865 |  2.6538 |  0.1207 |   0.7319 | -0.341  |
| agg_buy_hold |     2865 | -0.106  | -0.0098 |  -0.161  | -0.2337 |

---
_notes_: monthly rotation: SPY if 12M>SPY beats VEU & BIL; else VEU; else AGG