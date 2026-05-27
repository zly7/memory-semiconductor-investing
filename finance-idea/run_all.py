"""Refresh data → boot the dev stack (backend + frontend).

The old matplotlib pipeline (idea scripts → PNG → static report.html) was
replaced in v2 by a FastAPI + Vue 3 SPA. The legacy code lives under
`legacy/` and is not invoked from here anymore.

Usage:
    python run_all.py                # refresh, then start dev servers
    python run_all.py --no-refresh   # just start dev servers
    python run_all.py --refresh-only # refresh and exit
"""
from __future__ import annotations

import argparse
import os
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent
DATA_API = ROOT / "finance-data-api"
FRONTEND = ROOT / "frontend"


def run_refresh() -> None:
    print(f"[run_all] refreshing data via {DATA_API}/refresh.py …")
    t0 = time.time()
    subprocess.check_call([sys.executable, str(DATA_API / "refresh.py")])
    print(f"[run_all] refresh done in {time.time()-t0:.1f}s")


def run_dev() -> None:
    print("[run_all] starting backend + frontend (run_dev.sh) …")
    print("           backend  → http://127.0.0.1:8000  (docs /docs)")
    print("           frontend → http://localhost:5173")
    os.execv(str(ROOT / "run_dev.sh"), [str(ROOT / "run_dev.sh")])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--no-refresh", action="store_true")
    p.add_argument("--refresh-only", action="store_true")
    args = p.parse_args()
    if not args.no_refresh:
        run_refresh()
    if args.refresh_only:
        return
    run_dev()


if __name__ == "__main__":
    main()
