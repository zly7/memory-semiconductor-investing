"""Strategy module template.

Each strategy in `validation50/strategies/<id>.py` should look like this:

    from runner import StrategyMeta, Result, register, load_price, stats
    from ._helpers import (daily_returns, sma, switching_returns,
                           cash_ret_from_bil, bucket_fwd_returns,
                           classify_verdict, bucket_monotonicity)

    META = StrategyMeta(
        id="my_strategy_id",
        name_cn="...",
        family="trend",
        lit_verdict="robust",
    )

    @register(META.id)
    def compute() -> Result:
        # 1. Load data
        spy = load_price("SPY")
        bil = load_price("BIL")

        # 2. Build the signal
        signal = sma(spy, 200)

        # 3. Build the position / strategy returns (no look-ahead!)
        flag = (spy > signal).astype(float)
        cash = cash_ret_from_bil(bil, spy.index)
        strat = switching_returns(flag, daily_returns(spy), cash)

        # 4. Benchmarks
        bench = {"buy_hold_spy": daily_returns(spy)}

        # 5. Bucket / sanity table
        buckets = bucket_fwd_returns(signal=spy / signal - 1.0,
                                     asset=spy,
                                     horizons={"20d": 20, "60d": 60, "120d": 120})

        # 6. Verdict
        verdict, why = classify_verdict(META.lit_verdict,
                                        stats(strat), stats(bench["buy_hold_spy"]))

        return Result(
            meta=META,
            primary_series=signal,
            asset_series=spy,
            strategy_returns=strat,
            benchmark_returns=bench,
            buckets=buckets,
            verdict=verdict,
            verdict_why=why,
        )
"""
