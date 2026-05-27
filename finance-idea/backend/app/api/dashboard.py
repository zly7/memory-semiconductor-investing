"""GET /api/dashboard — current snapshot of all 10 signals."""
from __future__ import annotations

import datetime as dt

from fastapi import APIRouter

from ..schemas import DashboardResponse, SignalSnapshot
from ..signals import ORDER, REGISTRY

router = APIRouter()


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard() -> DashboardResponse:
    out: list[SignalSnapshot] = []
    for sid in ORDER:
        try:
            bundle = REGISTRY[sid]()
            out.append(bundle.snapshot())
        except Exception as e:  # noqa: BLE001
            out.append(SignalSnapshot(
                id=sid, name=sid, name_cn=sid,
                value=None, unit="", level="na",
                interpretation=f"error: {type(e).__name__}: {e}",
                spark=[],
            ))
    return DashboardResponse(asof=dt.datetime.now().isoformat(timespec="seconds"),
                             signals=out)
