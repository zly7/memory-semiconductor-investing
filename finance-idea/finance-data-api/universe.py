"""Symbol universe.

Each asset is tagged with class, source, vendor symbol and human label.
Adding/removing items here changes what `refresh.py` keeps up to date and what
the idea scripts can pull from the cache.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


Source = Literal["yfinance", "ak_etf", "ak_index", "ak_fund_nav",
                 "ak_bond_yield", "ak_north_flow", "ak_ah_premium",
                 "ak_hk_index", "ak_macro"]


@dataclass(frozen=True)
class Asset:
    key: str            # stable id used in code and filenames
    label: str          # human readable
    asset_class: str    # us_equity, cn_etf, qdii_etf, rate, fx, commodity, vol, sentiment, ...
    source: Source
    symbol: str         # vendor symbol passed to fetcher
    extras: tuple = ()  # extra fetches keyed by tag (e.g. ("nav",))


# -----------------------------------------------------------------------------
# US / global (yfinance)
# -----------------------------------------------------------------------------
US_EQUITY = [
    Asset("SPY",  "S&P 500 ETF",            "us_equity",  "yfinance", "SPY"),
    Asset("QQQ",  "Nasdaq 100 ETF",         "us_equity",  "yfinance", "QQQ"),
    Asset("IWM",  "Russell 2000 ETF",       "us_equity",  "yfinance", "IWM"),
    Asset("DIA",  "Dow Jones ETF",          "us_equity",  "yfinance", "DIA"),
    Asset("EEM",  "MSCI Emerging Mkts ETF", "us_equity",  "yfinance", "EEM"),
    Asset("FXI",  "China Large Cap ETF",    "us_equity",  "yfinance", "FXI"),
    Asset("ASHR", "CSI 300 ADR ETF",        "us_equity",  "yfinance", "ASHR"),
]

US_RATES_FX_COMMOD = [
    Asset("VIX",  "CBOE Volatility Index",      "vol",       "yfinance", "^VIX"),
    Asset("TNX",  "US 10Y Treasury Yield (x10)","rate",      "yfinance", "^TNX"),
    Asset("FVX",  "US  5Y Treasury Yield (x10)","rate",      "yfinance", "^FVX"),
    Asset("IRX",  "US 13W T-Bill (x10)",        "rate",      "yfinance", "^IRX"),
    Asset("TYX",  "US 30Y Treasury Yield (x10)","rate",      "yfinance", "^TYX"),
    Asset("DXY",  "US Dollar Index",            "fx",        "yfinance", "DX-Y.NYB"),
    Asset("GLD",  "Gold ETF",                   "commodity", "yfinance", "GLD"),
    Asset("SLV",  "Silver ETF",                 "commodity", "yfinance", "SLV"),
    Asset("USO",  "Oil ETF",                    "commodity", "yfinance", "USO"),
    Asset("HG",   "Copper Futures",             "commodity", "yfinance", "HG=F"),
    Asset("CL",   "Crude Oil Futures",          "commodity", "yfinance", "CL=F"),
    Asset("GC",   "Gold Futures",               "commodity", "yfinance", "GC=F"),
    Asset("BTC",  "Bitcoin",                    "crypto",    "yfinance", "BTC-USD"),
    Asset("TLT",  "20+Y Treasury ETF",          "us_equity", "yfinance", "TLT"),
]

# -----------------------------------------------------------------------------
# CN onshore indexes (akshare)
# -----------------------------------------------------------------------------
CN_INDEX = [
    Asset("SHCOMP",  "上证综指",   "cn_index", "ak_index", "sh000001"),
    Asset("CSI300",  "沪深300",    "cn_index", "ak_index", "sh000300"),
    Asset("CSI500",  "中证500",    "cn_index", "ak_index", "sh000905"),
    Asset("CHINEXT", "创业板指",   "cn_index", "ak_index", "sz399006"),
    Asset("STAR50",  "科创50",     "cn_index", "ak_index", "sh000688"),
]

# -----------------------------------------------------------------------------
# CN onshore ETFs (akshare hist + NAV)
# -----------------------------------------------------------------------------
CN_ETF = [
    Asset("ETF510300", "沪深300ETF (510300)",  "cn_etf", "ak_etf", "510300", extras=("nav",)),
    Asset("ETF510500", "中证500ETF (510500)",  "cn_etf", "ak_etf", "510500", extras=("nav",)),
    Asset("ETF159915", "创业板ETF (159915)",   "cn_etf", "ak_etf", "159915", extras=("nav",)),
    Asset("ETF588000", "科创50ETF (588000)",   "cn_etf", "ak_etf", "588000", extras=("nav",)),
    Asset("ETF510900", "H股ETF (510900)",      "cn_etf", "ak_etf", "510900", extras=("nav",)),
    Asset("ETF159740", "恒生科技ETF (159740)", "cn_etf", "ak_etf", "159740", extras=("nav",)),
    Asset("ETF518880", "黄金ETF (518880)",     "cn_etf", "ak_etf", "518880", extras=("nav",)),
]

# QDII ETFs — the heart of the premium-sentiment ideas.
QDII_ETF = [
    Asset("QDII513100", "纳指ETF 国泰 (513100)",      "qdii_etf", "ak_etf", "513100", extras=("nav",)),
    Asset("QDII513500", "标普500ETF 博时 (513500)",   "qdii_etf", "ak_etf", "513500", extras=("nav",)),
    Asset("QDII513300", "纳斯达克ETF 华夏 (513300)",  "qdii_etf", "ak_etf", "513300", extras=("nav",)),
    Asset("QDII159941", "纳指ETF 广发 (159941)",      "qdii_etf", "ak_etf", "159941", extras=("nav",)),
    Asset("QDII513880", "日经225ETF (513880)",         "qdii_etf", "ak_etf", "513880", extras=("nav",)),
    Asset("QDII513030", "德国30ETF (513030)",          "qdii_etf", "ak_etf", "513030", extras=("nav",)),
    Asset("QDII164906", "中概互联LOF (164906)",        "qdii_etf", "ak_etf", "513050", extras=("nav",)),
]

# -----------------------------------------------------------------------------
# Hong Kong (akshare)
# -----------------------------------------------------------------------------
HK_INDEX = [
    Asset("HSI",     "恒生指数",       "hk_index", "ak_hk_index", "HSI"),
    Asset("HSCEI",   "恒生中国企业",   "hk_index", "ak_hk_index", "HSCEI"),
    Asset("HSTECH",  "恒生科技指数",   "hk_index", "ak_hk_index", "HSTECH"),
]

# -----------------------------------------------------------------------------
# Macro / sentiment series (akshare specials)
# -----------------------------------------------------------------------------
MACRO_SENTIMENT = [
    Asset("CN_BOND_YIELD",  "中国国债收益率曲线",  "macro",     "ak_bond_yield",  "all"),
    Asset("AH_PREMIUM",     "恒生AH股溢价指数",    "sentiment", "ak_ah_premium",  "ahindex"),
    Asset("NORTH_FLOW",     "北向资金日净流入",    "sentiment", "ak_north_flow",  "北上"),
]


UNIVERSE: list[Asset] = (
    US_EQUITY
    + US_RATES_FX_COMMOD
    + CN_INDEX
    + CN_ETF
    + QDII_ETF
    + HK_INDEX
    + MACRO_SENTIMENT
)


def by_class(asset_class: str) -> list[Asset]:
    return [a for a in UNIVERSE if a.asset_class == asset_class]


def by_key(key: str) -> Asset:
    for a in UNIVERSE:
        if a.key == key:
            return a
    raise KeyError(key)


if __name__ == "__main__":
    from collections import Counter
    c = Counter(a.asset_class for a in UNIVERSE)
    print(f"Universe: {len(UNIVERSE)} assets")
    for k, v in sorted(c.items()):
        print(f"  {k:<14s} {v}")
