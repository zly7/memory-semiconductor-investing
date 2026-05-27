"""Signal registry — single source of truth for the 10 ideas."""
from __future__ import annotations

from . import (ah_premium, btc_gold, dxy_em, gold_copper, iwm_spy,
               northbound_flow, qdii_premium, qqq_ma200, vix_extreme,
               yield_curve)

REGISTRY = {
    "qdii_premium":   qdii_premium.compute,
    "qqq_ma200":      qqq_ma200.compute,
    "vix_extreme":    vix_extreme.compute,
    "gold_copper":    gold_copper.compute,
    "dxy_em":         dxy_em.compute,
    "yield_curve":    yield_curve.compute,
    "ah_premium":     ah_premium.compute,
    "northbound_flow": northbound_flow.compute,
    "iwm_spy":        iwm_spy.compute,
    "btc_gold":       btc_gold.compute,
}

ORDER = list(REGISTRY.keys())

__all__ = ["REGISTRY", "ORDER"]
