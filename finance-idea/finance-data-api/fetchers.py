"""Concrete fetchers.

Each fetcher returns a `pd.DataFrame` with a DatetimeIndex and well-known
columns (`open/high/low/close/volume` for price-like, single `value` column for
scalar series). Empty frame on transient failure — refresh.py logs and moves on.
"""
from __future__ import annotations

import time
import warnings
from datetime import date, datetime
from typing import Optional

import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)


# -----------------------------------------------------------------------------
# yfinance
# -----------------------------------------------------------------------------
def fetch_yf(symbol: str, start: str = "2015-01-01", retries: int = 3) -> pd.DataFrame:
    import yfinance as yf
    for i in range(retries):
        try:
            df = yf.download(symbol, start=start, progress=False, auto_adjust=False,
                             threads=False)
            if df is None or df.empty:
                time.sleep(1 + i)
                continue
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            df = df.rename(columns=str.lower)
            df.index.name = "date"
            keep = [c for c in ("open", "high", "low", "close", "adj close", "volume") if c in df.columns]
            df = df[keep].rename(columns={"adj close": "adj_close"})
            return df
        except Exception:
            time.sleep(1 + i)
    return pd.DataFrame()


# -----------------------------------------------------------------------------
# akshare — ETF daily OHLC
# -----------------------------------------------------------------------------
def _sina_etf_symbol(symbol: str) -> str:
    """Prefix bare ETF ticker with sh/sz for Sina endpoints."""
    if symbol.startswith(("sh", "sz")):
        return symbol
    if symbol.startswith(("5", "6", "9")):
        return "sh" + symbol
    return "sz" + symbol


def fetch_ak_etf(symbol: str, start: str = "20150101", retries: int = 3) -> pd.DataFrame:
    """Fetch ETF daily OHLC.

    Primary: ak.fund_etf_hist_sina (works even when the EM endpoint blackholes).
    Fallback: ak.fund_etf_hist_em.
    """
    import akshare as ak
    sina_sym = _sina_etf_symbol(symbol)
    end = datetime.now().strftime("%Y%m%d")
    for i in range(retries):
        try:
            df = ak.fund_etf_hist_sina(symbol=sina_sym)
            if df is None or df.empty:
                raise RuntimeError("empty")
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index("date").sort_index()
            keep = [c for c in ("open", "high", "low", "close", "volume", "amount") if c in df.columns]
            return df[keep].astype(float, errors="ignore")
        except Exception:
            time.sleep(1 + i)
    # fallback to EM
    for i in range(retries):
        try:
            df = ak.fund_etf_hist_em(symbol=symbol, period="daily",
                                     start_date=start, end_date=end, adjust="")
            if df is None or df.empty:
                time.sleep(1 + i)
                continue
            df = df.rename(columns={
                "日期": "date", "开盘": "open", "收盘": "close",
                "最高": "high", "最低": "low", "成交量": "volume",
                "成交额": "amount", "换手率": "turnover",
            })
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index("date").sort_index()
            return df[["open", "high", "low", "close", "volume", "amount", "turnover"]]
        except Exception:
            time.sleep(1 + i)
    return pd.DataFrame()


# -----------------------------------------------------------------------------
# akshare — A-share index daily
# -----------------------------------------------------------------------------
def fetch_ak_index(symbol: str, retries: int = 3) -> pd.DataFrame:
    """Fetch A-share index daily; Sina primary, EM fallback."""
    import akshare as ak
    for i in range(retries):
        try:
            df = ak.stock_zh_index_daily(symbol=symbol)  # Sina
            if df is None or df.empty:
                raise RuntimeError("empty")
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index("date").sort_index()
            keep = [c for c in ("open", "high", "low", "close", "volume") if c in df.columns]
            return df[keep].astype(float, errors="ignore")
        except Exception:
            time.sleep(1 + i)
    for i in range(retries):
        try:
            df = ak.stock_zh_index_daily_em(symbol=symbol)
            if df is None or df.empty:
                time.sleep(1 + i)
                continue
            df = df.rename(columns=str.lower)
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index("date").sort_index()
            return df[["open", "high", "low", "close", "volume"]]
        except Exception:
            time.sleep(1 + i)
    return pd.DataFrame()


# -----------------------------------------------------------------------------
# akshare — fund NAV time series (needed for QDII premium backtest)
# -----------------------------------------------------------------------------
def fetch_ak_fund_nav(symbol: str, start: str = "20150101", retries: int = 3) -> pd.DataFrame:
    import akshare as ak
    end = datetime.now().strftime("%Y%m%d")
    for i in range(retries):
        try:
            df = ak.fund_etf_fund_info_em(fund=symbol, start_date=start, end_date=end)
            if df is None or df.empty:
                time.sleep(1 + i)
                continue
            df = df.rename(columns={
                "净值日期": "date",
                "单位净值": "nav",
                "累计净值": "cum_nav",
                "日增长率": "daily_return_pct",
                "申购状态": "subscription_status",
                "赎回状态": "redemption_status",
            })
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index("date").sort_index()
            for c in ("nav", "cum_nav", "daily_return_pct"):
                if c in df.columns:
                    df[c] = pd.to_numeric(df[c], errors="coerce")
            return df
        except Exception:
            time.sleep(1 + i)
    return pd.DataFrame()


# -----------------------------------------------------------------------------
# akshare — China bond yield curve
# -----------------------------------------------------------------------------
def fetch_ak_bond_yield(retries: int = 3) -> pd.DataFrame:
    import akshare as ak
    for i in range(retries):
        try:
            df = ak.bond_china_yield(start_date="2015-01-01",
                                     end_date=datetime.now().strftime("%Y-%m-%d"))
            if df is None or df.empty:
                time.sleep(1 + i)
                continue
            # df has columns like 曲线名称, 日期, 3月, 6月, 1年, 3年, 5年, 7年, 10年, 30年
            df = df[df["曲线名称"] == "中债国债收益率曲线"].copy()
            df = df.rename(columns={"日期": "date"})
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index("date").sort_index()
            # Keep tenor columns
            tenors = [c for c in df.columns if c not in ("曲线名称",)]
            for c in tenors:
                df[c] = pd.to_numeric(df[c], errors="coerce")
            df = df[tenors]
            return df
        except Exception:
            time.sleep(1 + i)
    return pd.DataFrame()


# -----------------------------------------------------------------------------
# akshare — northbound flow daily
# -----------------------------------------------------------------------------
def fetch_ak_north_flow(retries: int = 3) -> pd.DataFrame:
    import akshare as ak
    candidates = [
        ("stock_hsgt_hist_em", {"symbol": "北向资金"}),
        ("stock_hsgt_north_net_flow_in_em", {"symbol": "北上"}),
    ]
    for name, kwargs in candidates:
        if not hasattr(ak, name):
            continue
        for i in range(retries):
            try:
                df = getattr(ak, name)(**kwargs)
                if df is None or df.empty:
                    time.sleep(1)
                    continue
                df = df.copy()
                # Find date column
                date_col = next((c for c in df.columns
                                 if c in ("日期", "date") or "日期" in c), None)
                if not date_col:
                    return pd.DataFrame()
                df = df.rename(columns={date_col: "date"})
                df["date"] = pd.to_datetime(df["date"])
                df = df.set_index("date").sort_index()
                # numeric coercion for the rest
                for c in df.columns:
                    df[c] = pd.to_numeric(df[c], errors="coerce")
                return df
            except Exception:
                time.sleep(1 + i)
    return pd.DataFrame()


# -----------------------------------------------------------------------------
# akshare — AH premium index
# -----------------------------------------------------------------------------
def fetch_ak_ah_premium(retries: int = 3) -> pd.DataFrame:
    """Constructs AH premium index history from per-stock A/H pair series.

    ak doesn't expose the official Hang Seng AH premium index daily directly
    in all versions; we fall back to ak.stock_zh_ah_daily for per-pair history
    *if available* or stock_zh_ah_spot for the latest snapshot.
    """
    import akshare as ak
    # Prefer the dedicated index hist if present
    if hasattr(ak, "stock_hk_ah_premium_index"):
        try:
            df = ak.stock_hk_ah_premium_index()
            if df is not None and not df.empty:
                df = df.rename(columns={"日期": "date", "ah_index": "ah_premium"})
                df["date"] = pd.to_datetime(df["date"])
                return df.set_index("date").sort_index()
        except Exception:
            pass
    # Fallback: use the ETF tracking it (159509 is not a premium tracker; instead
    # we derive an index from the spot snapshot if hist is unavailable).
    if hasattr(ak, "stock_hk_ah_index_em"):
        try:
            df = ak.stock_hk_ah_index_em()
            df = df.rename(columns={"日期": "date"})
            df["date"] = pd.to_datetime(df["date"])
            return df.set_index("date").sort_index()
        except Exception:
            pass
    return pd.DataFrame()


# -----------------------------------------------------------------------------
# akshare — HK index history
# -----------------------------------------------------------------------------
def fetch_ak_hk_index(symbol: str, retries: int = 3) -> pd.DataFrame:
    """HK index daily — Sina primary."""
    import akshare as ak
    for i in range(retries):
        try:
            df = ak.stock_hk_index_daily_sina(symbol=symbol)
            if df is None or df.empty:
                raise RuntimeError("empty")
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index("date").sort_index()
            keep = [c for c in ("open", "high", "low", "close", "volume") if c in df.columns]
            return df[keep].astype(float, errors="ignore")
        except Exception:
            time.sleep(1 + i)
    for i in range(retries):
        try:
            df = ak.stock_hk_index_daily_em(symbol=symbol)
            if df is None or df.empty:
                time.sleep(1 + i)
                continue
            df = df.rename(columns=str.lower)
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index("date").sort_index()
            keep = [c for c in ("open", "high", "low", "close", "latest") if c in df.columns]
            if "latest" in keep and "close" not in df.columns:
                df["close"] = df["latest"]
            return df
        except Exception:
            time.sleep(1 + i)
    return pd.DataFrame()


# -----------------------------------------------------------------------------
# Real-time snapshot — used by ideas/01 and the dashboard for current premium
# -----------------------------------------------------------------------------
def fetch_etf_spot_snapshot() -> pd.DataFrame:
    """Returns a snapshot dataframe of ALL onshore ETFs with IOPV/premium.

    Column convention:
        code, name, price, iopv, discount_pct  (negative discount = premium)
    """
    import akshare as ak
    df = ak.fund_etf_spot_em()
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.rename(columns={
        "代码": "code", "名称": "name", "最新价": "price",
        "IOPV实时估值": "iopv", "基金折价率": "discount_pct",
    })[["code", "name", "price", "iopv", "discount_pct"]]
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["iopv"] = pd.to_numeric(df["iopv"], errors="coerce")
    df["discount_pct"] = pd.to_numeric(df["discount_pct"], errors="coerce")
    df["premium_pct"] = (df["price"] - df["iopv"]) / df["iopv"] * 100
    return df


__all__ = [
    "fetch_yf", "fetch_ak_etf", "fetch_ak_index", "fetch_ak_fund_nav",
    "fetch_ak_bond_yield", "fetch_ak_north_flow", "fetch_ak_ah_premium",
    "fetch_ak_hk_index", "fetch_etf_spot_snapshot",
]
