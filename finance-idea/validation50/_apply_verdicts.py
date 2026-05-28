"""Stamp scorecard.json verdicts back into FEATURE_LIST.md.

Replaces `| tbd | todo |` (and similar placeholders) on each strategy row with
the actual `our_verdict` + status. Idempotent: re-running after a fresh runner
pass keeps the table in sync.
"""
from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
data = json.loads((ROOT / "outputs" / "scorecard.json").read_text(encoding="utf-8"))
verdict_by_id = {r["id"]: r for r in data if r.get("status") == "ok" or r.get("our_verdict")}

feat = ROOT / "FEATURE_LIST.md"
lines = feat.read_text(encoding="utf-8").splitlines()

# Find each row containing a `<id>` backtick token and replace the trailing
# two pipe-fields with our verdict + status.
ROW_RE = re.compile(r"^(\|\s*\d+\s*\|\s*`(?P<id>[a-z0-9_]+)`.*?)\|\s*tbd\s*\|\s*(?:todo|data-needed|wip)\s*\|\s*$",
                    re.IGNORECASE)
TRAIL_RE = re.compile(r"^(\|\s*\d+\s*\|\s*`(?P<id>[a-z0-9_]+)`.*?)\|\s*[^|]*\|\s*(?:done|skipped)\s*\|\s*$",
                      re.IGNORECASE)

n_updated = 0
for i, line in enumerate(lines):
    m = ROW_RE.match(line) or TRAIL_RE.match(line)
    if not m:
        continue
    sid = m.group("id")
    if sid not in verdict_by_id:
        continue
    r = verdict_by_id[sid]
    verdict = r.get("our_verdict") or "tbd"
    status = "skipped" if verdict == "skipped" else "done"
    new_tail = f"| {verdict} | {status} |"
    lines[i] = re.sub(r"\|\s*[^|]*\|\s*[^|]*\|\s*$", new_tail, line)
    n_updated += 1

feat.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Updated {n_updated} rows in {feat.name}")
