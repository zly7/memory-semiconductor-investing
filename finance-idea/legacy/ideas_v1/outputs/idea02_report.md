# Idea 02 — Buy QQQ when below its 200-day SMA

Latest QQQ 730.28, SMA200 617.15, ratio 1.183
Above-SMA regime currently active.

## Forward return by close/SMA200 ratio bucket
| close     |    n |   fwd20_mean |   fwd60_mean |   fwd60_win |
|:----------|-----:|-------------:|-------------:|------------:|
| ≤0.85     |   62 |       0.0457 |       0.0463 |      0.5968 |
| 0.85-0.95 |  253 |       0.0189 |       0.0473 |      0.6245 |
| 0.95-1.00 |  209 |       0.0053 |       0.0352 |      0.6986 |
| 1.00-1.05 |  346 |       0.018  |       0.0645 |      0.737  |
| 1.05-1.15 | 1583 |       0.0159 |       0.0406 |      0.7669 |
| >1.15     |  321 |       0.0043 |       0.0322 |      0.6293 |

## Strategy stats
| name                          |   n_days |   total |   cagr |   sharpe |   maxdd |
|:------------------------------|---------:|--------:|-------:|---------:|--------:|
| QQQ buy & hold                |     2973 |  6.0942 | 0.1807 |   0.8813 | -0.3562 |
| Long only when close ≤ SMA200 |     2973 |  0.2326 | 0.0179 |   0.195  | -0.318  |
| Long only when close > SMA200 |     2973 |  4.5868 | 0.157  |   1.0332 | -0.2188 |

Read-out: buy-the-dip generally underperforms buy-and-hold over the full
sample (you miss the strongest trend days), but its **per-day-invested**
return is informative for tactical sizing.