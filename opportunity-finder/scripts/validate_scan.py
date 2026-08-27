#!/usr/bin/env python3
"""Validate exploration coverage and traceability for Opportunity Finder scans.

Usage:
  python scripts/validate_scan.py candidates.json scored.json --pretty

The validator does not decide which opportunity is best. It checks whether a
broad scan explored enough workflow domains, performed at least one traceable
Winner Benchmark, and kept public-web evidence auditable before concluding
"nothing worth shipping today".
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "criteria.json"
URL_RE = re.compile(r"^https?://", re.I)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def candidates_from(payload):
    if isinstance(payload, dict):
        return payload.get("candidates", [])
    return payload


def _valid_date(value):
    return isinstance(value, str) and bool(DATE_RE.match(value.strip()))


def _traceable_source(ev):
    if not isinstance(ev, dict):
        return False
    ref = str(ev.get("source_reference", "")).strip()
    observed = ev.get("observed_at") or ev.get("observation_date")
    return bool(URL_RE.match(ref)) and _valid_date(observed)


def _candidate_traceable(c, min_sources):
    evidence = c.get("evidence", []) if isinstance(c, dict) else []
    count = sum(1 for ev in evidence if _traceable_source(ev))
    return count >= min_sources, count


def _winner_traceable(w):
    if not isinstance(w, dict):
        return False
    ref = str(w.get("source_reference", "")).strip()
    observed = w.get("observation_date") or w.get("observed_at")
    job = str(w.get("job_to_be_done", "")).strip()
    notes = str(w.get("signal_quality_notes", "")).strip()
    adjacent = str(w.get("adjacent_unresolved_job", "")).strip()
    return bool(URL_RE.match(ref)) and _valid_date(observed) and bool(job and notes and adjacent)


def validate(candidates_payload, scored_payload, config):
    candidates = candidates_from(candidates_payload)
    if not isinstance(candidates, list):
        raise ValueError("Candidate input must be a list or {'candidates': [...]} object")

    results = scored_payload.get("results", []) if isinstance(scored_payload, dict) else []
    result_by_name = {r.get("name"): r for r in results if isinstance(r, dict)}

    declared_scope = "broad"
    winner_benchmarks = []
    if isinstance(candidates_payload, dict):
        declared_scope = candidates_payload.get("scan_scope", "broad")
        winner_benchmarks = candidates_payload.get("winner_benchmarks", []) or []

    domains = sorted({str(c.get("domain", "")).strip() for c in candidates if str(c.get("domain", "")).strip()})
    min_domains = int(config.get("broad_scan_min_distinct_domains", 4))
    min_winners = int(config.get("broad_scan_min_winner_benchmarks", 1))
    min_sources = int(config.get("minimum_traceable_sources_per_candidate", 1))
    min_traceable_ratio = float(config.get("broad_scan_min_traceable_candidate_ratio", 1.0))
    ships = [r for r in results if r.get("decision") == "SHIP"]

    platform_incident_count = 0
    for c in candidates:
        rc = c.get("root_cause", {}) or {}
        flags = c.get("flags", {}) or {}
        if rc.get("platform_incident_only") or flags.get("platform_incident_only"):
            platform_incident_count += 1

    core_agent_count = sum(1 for c in candidates if c.get("domain") == "core-agent-dev")
    killed_core = 0
    for c in candidates:
        if c.get("domain") != "core-agent-dev":
            continue
        r = result_by_name.get(c.get("name"), {})
        if r.get("decision") in {"SKIP", "WATCH"}:
            killed_core += 1
    core_kill_ratio = round(killed_core / core_agent_count, 3) if core_agent_count else 0.0

    traceable_candidates = 0
    candidate_source_counts = {}
    for c in candidates:
        ok, count = _candidate_traceable(c, min_sources)
        candidate_source_counts[str(c.get("name", ""))] = count
        traceable_candidates += int(ok)
    traceable_ratio = round(traceable_candidates / len(candidates), 3) if candidates else 1.0

    traceable_winners = sum(1 for w in winner_benchmarks if _winner_traceable(w))

    complete = True
    reasons = []
    if declared_scope == "broad" and len(domains) < min_domains:
        complete = False
        reasons.append(f"broad scan covered {len(domains)} domains; minimum is {min_domains}")
    if declared_scope == "broad" and traceable_winners < min_winners:
        complete = False
        reasons.append(f"broad scan has {traceable_winners} traceable Winner Benchmarks; minimum is {min_winners}")
    if declared_scope == "broad" and traceable_ratio < min_traceable_ratio:
        complete = False
        reasons.append(
            f"only {traceable_ratio:.0%} of candidates have the required traceable original-source evidence; minimum is {min_traceable_ratio:.0%}"
        )
    if declared_scope == "broad" and not ships and core_agent_count and core_kill_ratio >= 0.7 and len(domains) < min_domains + 1:
        complete = False
        reasons.append("core-agent candidates were mostly killed; expand into adjacent professional workflows before declaring zero-SHIP")

    return {
        "scan_scope": declared_scope,
        "candidate_count": len(candidates),
        "distinct_domains": domains,
        "distinct_domain_count": len(domains),
        "minimum_domains_for_broad_scan": min_domains,
        "ship_count": len(ships),
        "platform_incident_candidate_count": platform_incident_count,
        "core_agent_candidate_count": core_agent_count,
        "core_agent_watch_or_skip_ratio": core_kill_ratio,
        "winner_benchmark_count": len(winner_benchmarks),
        "traceable_winner_benchmark_count": traceable_winners,
        "minimum_traceable_winner_benchmarks": min_winners,
        "traceable_candidate_count": traceable_candidates,
        "traceable_candidate_ratio": traceable_ratio,
        "minimum_traceable_candidate_ratio": min_traceable_ratio,
        "candidate_traceable_source_counts": candidate_source_counts,
        "scan_complete": complete,
        "incomplete_reasons": reasons,
    }


def main():
    ap = argparse.ArgumentParser(description="Validate Opportunity Finder scan coverage and source traceability")
    ap.add_argument("candidates", type=Path)
    ap.add_argument("scored", type=Path)
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    ap.add_argument("--pretty", action="store_true")
    args = ap.parse_args()
    out = validate(load_json(args.candidates), load_json(args.scored), load_json(args.config))
    print(json.dumps(out, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0 if out["scan_complete"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
