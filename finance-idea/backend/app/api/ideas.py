"""GET /api/ideas, GET /api/ideas/{id}."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..schemas import IdeaDetail, IdeaSummary
from ..signals import ORDER, REGISTRY

router = APIRouter()


@router.get("/ideas", response_model=list[IdeaSummary])
def list_ideas() -> list[IdeaSummary]:
    out = []
    for sid in ORDER:
        try:
            b = REGISTRY[sid]()
            out.append(IdeaSummary(
                id=b.id, name=b.name, name_cn=b.name_cn,
                description=b.description,
                tags=[]
            ))
        except Exception:
            out.append(IdeaSummary(id=sid, name=sid, name_cn=sid,
                                    description=""))
    return out


@router.get("/ideas/{idea_id}", response_model=IdeaDetail)
def get_idea(idea_id: str) -> IdeaDetail:
    if idea_id not in REGISTRY:
        raise HTTPException(404, detail=f"unknown idea id: {idea_id}")
    try:
        bundle = REGISTRY[idea_id]()
    except Exception as e:  # noqa: BLE001
        raise HTTPException(500, detail=f"signal compute failed: {e}") from e
    return bundle.detail()
