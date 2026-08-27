#!/usr/bin/env python3
"""Local-only Opportunity Finder run/outcome ledger.

No network calls. Records coarse structured fields to a JSONL file so the user can
learn from their own opportunity decisions over time.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_PATH = Path.home() / ".opportunity-finder" / "history.jsonl"
ALLOWED_FIELDS = {
    "event", "timestamp", "candidate_id", "name", "coarse_category", "decision",
    "portfolio_role", "suggested_price_usd", "build_hours", "channel",
    "installed", "paid_sales", "revenue_usd", "status", "notes_code"
}
ALLOWED_EVENTS = {"scan", "candidate", "launch", "outcome"}


def sanitize(record: dict) -> dict:
    if not isinstance(record, dict):
        raise ValueError("record must be a JSON object")
    unknown = set(record) - ALLOWED_FIELDS
    if unknown:
        raise ValueError("unsupported fields: " + ", ".join(sorted(unknown)))
    event = record.get("event")
    if event not in ALLOWED_EVENTS:
        raise ValueError(f"unsupported event: {event}")
    out = dict(record)
    out.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    return out


def append_record(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    clean = sanitize(record)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(clean, ensure_ascii=False, separators=(",", ":")) + "\n")


def read_records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def summarize(records: list[dict]) -> dict:
    decisions = Counter(r.get("decision") for r in records if r.get("decision"))
    statuses = Counter(r.get("status") for r in records if r.get("status"))
    sales = sum(float(r.get("paid_sales", 0) or 0) for r in records)
    revenue = sum(float(r.get("revenue_usd", 0) or 0) for r in records)
    return {
        "records": len(records),
        "decisions": dict(decisions),
        "statuses": dict(statuses),
        "paid_sales_total": round(sales, 2),
        "revenue_usd_total": round(revenue, 2),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Local Opportunity Finder history ledger")
    parser.add_argument("--path", type=Path, default=DEFAULT_PATH)
    sub = parser.add_subparsers(dest="command", required=True)
    a = sub.add_parser("append")
    a.add_argument("record_json", type=Path)
    sub.add_parser("summary")
    args = parser.parse_args()

    if args.command == "append":
        record = json.loads(args.record_json.read_text(encoding="utf-8"))
        append_record(args.path, record)
        print(json.dumps({"written": True, "path": str(args.path)}, ensure_ascii=False))
    else:
        print(json.dumps(summarize(read_records(args.path)), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
