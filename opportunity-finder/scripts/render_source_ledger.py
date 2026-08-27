#!/usr/bin/env python3
"""Render a deterministic, clickable Markdown Source Ledger from Opportunity Finder scan JSON."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse


def is_http_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def safe(text: object) -> str:
    if text is None:
        return ""
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def collect(scan: dict) -> list[dict]:
    rows: list[dict] = []
    seen: set[tuple[str, str, str]] = set()

    for wb in scan.get("winner_benchmarks", []) or []:
        url = wb.get("source_reference")
        if not is_http_url(url):
            continue
        date = wb.get("source_date") or wb.get("observed_at") or wb.get("observation_date") or ""
        supports = wb.get("job_to_be_done") or wb.get("product") or wb.get("product_name") or "winner benchmark"
        key = ("winner", url, safe(supports))
        if key in seen:
            continue
        seen.add(key)
        rows.append({"claim_type": "winner", "url": url, "source_date": date, "observed_at": wb.get("observed_at") or wb.get("observation_date") or "", "supports": supports})

    for cand in scan.get("candidates", []) or []:
        cname = cand.get("name", "candidate")
        for ev in cand.get("evidence", []) or []:
            url = ev.get("source_reference")
            if not is_http_url(url):
                continue
            claim = ev.get("claim_type") or "other"
            supports = ev.get("note") or ev.get("pain") or f"{cname}: {claim}"
            key = (str(claim), url, safe(supports))
            if key in seen:
                continue
            seen.add(key)
            rows.append({"claim_type": claim, "url": url, "source_date": ev.get("source_date") or "", "observed_at": ev.get("observed_at") or "", "supports": supports})
    return rows


def render(rows: list[dict]) -> str:
    out = ["## Source Ledger", "", "| ID | Claim type | Source | Source date | Observed | Supports |", "|---|---|---|---|---|---|"]
    for i, row in enumerate(rows, 1):
        url = row["url"]
        host = urlparse(url).netloc or "source"
        link = f"[{safe(host)}]({url})"
        out.append(f"| S{i} | {safe(row['claim_type'])} | {link} | {safe(row['source_date']) or '—'} | {safe(row['observed_at']) or '—'} | {safe(row['supports'])} |")
    if not rows:
        out.append("| — | — | — | — | — | No traceable HTTP(S) sources found. |")
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("scan_json")
    ap.add_argument("--output", "-o")
    args = ap.parse_args()
    scan = json.loads(Path(args.scan_json).read_text(encoding="utf-8"))
    text = render(collect(scan))
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
