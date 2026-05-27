#!/usr/bin/env bash
# Boot the FastAPI backend and Vite frontend together for development.
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  echo "create the venv first: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt fastapi uvicorn"
  exit 1
fi

# shellcheck disable=SC1091
source .venv/bin/activate

cleanup() {
  echo
  echo "shutting down…"
  jobs -p | xargs -r kill 2>/dev/null || true
}
trap cleanup EXIT INT TERM

uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!
echo "backend  → http://127.0.0.1:8000 (docs at /docs)  pid=$BACKEND_PID"

(cd frontend && npm run dev) &
FRONT_PID=$!
echo "frontend → http://localhost:5173                  pid=$FRONT_PID"

wait
