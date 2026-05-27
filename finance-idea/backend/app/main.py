"""FastAPI app factory."""
from __future__ import annotations

import pathlib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .api import dashboard, ideas, meta, series

app = FastAPI(title="finance-idea API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router, prefix="/api", tags=["dashboard"])
app.include_router(ideas.router, prefix="/api", tags=["ideas"])
app.include_router(series.router, prefix="/api", tags=["series"])
app.include_router(meta.router, prefix="/api", tags=["meta"])


# Optionally serve the built SPA (frontend/dist) when present
FRONT_DIST = pathlib.Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if FRONT_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONT_DIST / "assets"), name="assets")

    @app.get("/")
    def spa_index() -> FileResponse:
        return FileResponse(FRONT_DIST / "index.html")

    @app.get("/{full_path:path}")
    def spa_catch_all(full_path: str) -> FileResponse:
        # don't shadow /api
        if full_path.startswith("api"):
            return FileResponse(FRONT_DIST / "index.html",
                                status_code=404)
        target = FRONT_DIST / full_path
        if target.exists() and target.is_file():
            return FileResponse(target)
        return FileResponse(FRONT_DIST / "index.html")
else:
    @app.get("/")
    def root() -> dict:
        return {
            "service": "finance-idea",
            "docs": "/docs",
            "frontend": "run `cd frontend && npm run dev` for the SPA",
            "endpoints": [
                "GET /api/dashboard",
                "GET /api/ideas",
                "GET /api/ideas/{id}",
                "GET /api/series/{key}",
                "GET /api/meta",
                "GET /api/ticker",
            ],
        }
