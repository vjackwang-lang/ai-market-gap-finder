#!/usr/bin/env python3
"""Deterministically score Quick-Commerce Opportunity Finder candidates.

Usage:
    python scripts/score_opportunities.py candidates.json --pretty

Input may be a JSON list or {"candidates": [...]}.
Standard library only.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "criteria.json"
URL_RE = re.compile(r"^https?://", re.I)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def traceable_evidence_count(candidate: dict) -> int:
    count = 0
    for ev in candidate.get("evidence", []) or []:
        if not isinstance(ev, dict):
            continue
        ref = str(ev.get("source_reference", "")).strip()
        observed = ev.get("observed_at") or ev.get("observation_date")
        if URL_RE.match(ref) and isinstance(observed, str) and DATE_RE.match(observed.strip()):
            count += 1
    return count


def load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise SystemExit(f"File not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}")


def clamp_score(value, key: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"Score '{key}' must be a number from 0 to 10")
    if not 0 <= float(value) <= 10:
        raise ValueError(f"Score '{key}' must be between 0 and 10, got {value}")
    return float(value)


def nonnegative_number(value, key: str, default: float = 0.0) -> float:
    if value is None:
        return float(default)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"'{key}' must be a non-negative number")
    value = float(value)
    if value < 0:
        raise ValueError(f"'{key}' must be non-negative")
    return value


def compute_economics(candidate: dict, config: dict) -> dict:
    econ = candidate.get("economics", {}) or {}
    build_hours = nonnegative_number(econ.get("build_hours"), "build_hours")
    cash_cost = nonnegative_number(econ.get("cash_cost_usd"), "cash_cost_usd")
    hourly_rate = nonnegative_number(
        econ.get("internal_hourly_rate_usd", config.get("default_internal_hourly_rate_usd", 25)),
        "internal_hourly_rate_usd",
    )
    price = nonnegative_number(econ.get("suggested_price_usd"), "suggested_price_usd")
    fee_pct = nonnegative_number(
        econ.get("platform_fee_pct", config.get("default_platform_fee_pct", 20)),
        "platform_fee_pct",
    )
    if fee_pct > 100:
        raise ValueError("'platform_fee_pct' cannot exceed 100")
    variable_cost = nonnegative_number(
        econ.get("variable_cost_per_paid_user_usd"), "variable_cost_per_paid_user_usd"
    )

    dev_cost = cash_cost + build_hours * hourly_rate
    net_per_sale = max(0.0, price * (1.0 - fee_pct / 100.0) - variable_cost)
    breakeven = None
    if price > 0 and net_per_sale > 0:
        breakeven = int(math.ceil(dev_cost / net_per_sale))

    return {
        "build_hours": round(build_hours, 2),
        "cash_cost_usd": round(cash_cost, 2),
        "estimated_dev_cost_usd": round(dev_cost, 2),
        "suggested_price_usd": round(price, 2),
        "platform_fee_pct": round(fee_pct, 2),
        "variable_cost_per_paid_user_usd": round(variable_cost, 4),
        "net_revenue_per_sale_usd": round(net_per_sale, 2),
        "breakeven_paid_users": breakeven,
        "runtime_model_cost_owner": econ.get("runtime_model_cost_owner", "unknown"),
        "portfolio_role": econ.get("portfolio_role", "unspecified")
    }


def score_candidate(candidate: dict, config: dict) -> dict:
    name = candidate.get("name", "unnamed")
    scores = candidate.get("scores", {})
    flags = candidate.get("flags", {})

    missing = [key for key in config["weights"] if key not in scores]
    if missing:
        raise ValueError(f"Candidate '{name}' missing scores: {', '.join(missing)}")

    weighted = 0.0
    breakdown = {}
    for key, weight in config["weights"].items():
        raw = clamp_score(scores[key], key)
        contribution = raw / 10.0 * float(weight)
        weighted += contribution
        breakdown[key] = round(contribution, 2)

    hard_reasons = [flag for flag in config["hard_reject_flags"] if bool(flags.get(flag, False))]
    for flag in config.get("legacy_hard_reject_flags", []):
        if bool(flags.get(flag, False)) and flag not in hard_reasons:
            hard_reasons.append(flag)
    penalty_total = 0.0
    applied_penalties = {}
    for flag, points in config["penalties"].items():
        if bool(flags.get(flag, False)):
            penalty_total += float(points)
            applied_penalties[flag] = float(points)

    # Competition maturity is explicit in V1.4. A few fresh alternatives validate a
    # market but do not deserve the same penalty as a mature, adopted free incumbent.
    competition = candidate.get("competition", {}) or {}
    maturity = competition.get("maturity")
    if maturity is not None:
        allowed_maturity = set(config.get("competition_maturity_levels", []))
        if maturity not in allowed_maturity:
            raise ValueError(
                f"'competition.maturity' must be one of {sorted(allowed_maturity)}, got {maturity!r}"
            )
        if maturity == "mature":
            key = "mature_free_incumbent"
            if key not in applied_penalties:
                pts = float(config.get("penalties", {}).get(key, 0))
                penalty_total += pts
                applied_penalties[key] = pts
        elif maturity == "emerging":
            key = "emerging_free_alternatives"
            if "mature_free_incumbent" not in applied_penalties and key not in applied_penalties:
                pts = float(config.get("penalties", {}).get(key, 0))
                penalty_total += pts
                applied_penalties[key] = pts

    root_cause = candidate.get("root_cause", {}) or {}
    if bool(root_cause.get("platform_incident_only", False)) and "platform_incident_only" not in hard_reasons:
        hard_reasons.append("platform_incident_only")

    final_score = max(0.0, min(100.0, weighted - penalty_total))
    evidence_count = candidate.get("evidence_count", 0)
    try:
        evidence_count = int(evidence_count)
    except (TypeError, ValueError):
        evidence_count = 0
    traceable_count = traceable_evidence_count(candidate)

    economics = compute_economics(candidate, config)
    # Quick-Commerce mode values time. If declared build hours exceed the hard limit,
    # reject even if the caller forgot to set the flag.
    hard_hours = float(config.get("hard_build_hours_max", 24))
    if economics["build_hours"] > hard_hours and "build_over_hard_limit" not in hard_reasons:
        hard_reasons.append("build_over_hard_limit")

    # A FREE_ANCHOR must buy a measurable portfolio asset. If not declared, penalize it
    # automatically rather than treating "free" as a business model by itself.
    if economics.get("portfolio_role") == "FREE_ANCHOR":
        targets = candidate.get("free_asset_targets", []) or []
        allowed = set(config.get("free_asset_targets", []))
        valid_targets = [x for x in targets if x in allowed]
        if not valid_targets and "free_without_asset" not in applied_penalties:
            pts = float(config.get("penalties", {}).get("free_without_asset", 0))
            penalty_total += pts
            applied_penalties["free_without_asset"] = pts
            final_score = max(0.0, min(100.0, weighted - penalty_total))

    evidence_quality = float(scores.get("evidence_quality", 0))
    technical_feasibility = float(scores.get("technical_feasibility", 0))
    workaround_friction = float(scores.get("workaround_friction", 0))
    implementation = candidate.get("implementation", {}) or {}
    build_estimate_confidence = implementation.get("build_estimate_confidence", 0.0)
    if isinstance(build_estimate_confidence, bool) or not isinstance(build_estimate_confidence, (int, float)):
        raise ValueError("'build_estimate_confidence' must be a number from 0 to 1")
    build_estimate_confidence = float(build_estimate_confidence)
    if not 0 <= build_estimate_confidence <= 1:
        raise ValueError("'build_estimate_confidence' must be between 0 and 1")

    min_build_conf = float(config.get("minimum_build_estimate_confidence_for_ship", 0))
    if build_estimate_confidence < min_build_conf and "low_build_estimate_confidence" not in applied_penalties:
        pts = float(config.get("penalties", {}).get("low_build_estimate_confidence", 0))
        penalty_total += pts
        applied_penalties["low_build_estimate_confidence"] = pts
        final_score = max(0.0, min(100.0, weighted - penalty_total))

    workaround_minutes = implementation.get("workaround_minutes")
    if workaround_minutes is not None:
        workaround_minutes = nonnegative_number(workaround_minutes, "workaround_minutes")
        if workaround_minutes <= float(config.get("trivial_workaround_minutes_max", 0)) and "trivial_workaround" not in applied_penalties:
            pts = float(config.get("penalties", {}).get("trivial_workaround", 0))
            penalty_total += pts
            applied_penalties["trivial_workaround"] = pts
            final_score = max(0.0, min(100.0, weighted - penalty_total))

    surface_accessible = implementation.get("surface_accessible")
    if surface_accessible is False and "inaccessible_required_surface" not in hard_reasons:
        hard_reasons.append("inaccessible_required_surface")

    implementation_path_verified = implementation.get("implementation_path_verified")
    if implementation_path_verified is False and "no_concrete_implementation_path" not in hard_reasons:
        hard_reasons.append("no_concrete_implementation_path")

    if hard_reasons:
        decision = "SKIP"
    elif final_score >= config["decision_bands"]["ship"]:
        enough_count = evidence_count >= config["minimum_independent_evidence_for_ship"]
        enough_traceable = traceable_count >= int(config.get("minimum_traceable_sources_for_ship", config.get("minimum_independent_evidence_for_ship", 2)))
        enough_quality = evidence_quality >= float(config.get("minimum_evidence_quality_for_ship", 0))
        enough_technical = technical_feasibility >= float(config.get("minimum_technical_feasibility_for_ship", 0))
        enough_workaround = workaround_friction >= float(config.get("minimum_workaround_friction_for_ship", 0))
        enough_build_confidence = build_estimate_confidence >= min_build_conf
        enough_surface = surface_accessible is True
        enough_implementation_path = implementation_path_verified is True
        if enough_count and enough_traceable and enough_quality and enough_technical and enough_workaround and enough_build_confidence and enough_surface and enough_implementation_path:
            decision = "SHIP"
        else:
            decision = "TEST"
    elif final_score >= config["decision_bands"]["test"]:
        decision = "TEST"
    elif final_score >= config["decision_bands"]["watch"]:
        decision = "WATCH"
    else:
        decision = "SKIP"

    result = dict(candidate)
    result["weighted_score"] = round(final_score, 2)
    result["decision"] = decision
    result["score_breakdown"] = breakdown
    result["penalties_applied"] = applied_penalties
    result["hard_reject_reasons"] = hard_reasons
    result["evidence_traceability"] = {
        "declared_evidence_count": evidence_count,
        "traceable_original_source_count": traceable_count,
        "minimum_traceable_sources_for_ship": int(config.get("minimum_traceable_sources_for_ship", config.get("minimum_independent_evidence_for_ship", 2))),
    }
    result["economics_summary"] = economics
    result["implementation_summary"] = {
        "build_estimate_confidence": round(build_estimate_confidence, 2),
        "required_surfaces": implementation.get("required_surfaces", []),
        "stable_interfaces": implementation.get("stable_interfaces", []),
        "test_path": implementation.get("test_path", ""),
        "workaround_minutes": workaround_minutes,
        "surface_accessible": surface_accessible,
        "implementation_path_verified": implementation_path_verified,
    }
    result["competition_summary"] = {
        "maturity": competition.get("maturity", "unspecified"),
        "free_alternative_count": competition.get("free_alternative_count"),
        "dominant_free_incumbent": competition.get("dominant_free_incumbent"),
        "notes": competition.get("notes", ""),
    }
    result["root_cause_summary"] = {
        "platform_incident_only": bool(root_cause.get("platform_incident_only", False)),
        "user_controlled_fix": root_cause.get("user_controlled_fix"),
        "notes": root_cause.get("notes", ""),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Score Quick-Commerce opportunity candidates")
    parser.add_argument("input", type=Path, help="Candidate JSON file")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Criteria JSON")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = parser.parse_args()

    config = load_json(args.config)
    payload = load_json(args.input)
    candidates = payload.get("candidates", []) if isinstance(payload, dict) else payload
    if not isinstance(candidates, list):
        raise SystemExit("Input must be a list or an object containing a 'candidates' list")

    results = []
    try:
        for candidate in candidates:
            if not isinstance(candidate, dict):
                raise ValueError("Each candidate must be a JSON object")
            results.append(score_candidate(candidate, config))
    except ValueError as exc:
        print(f"Validation error: {exc}", file=sys.stderr)
        return 2

    results.sort(key=lambda x: x["weighted_score"], reverse=True)
    out = {"criteria_version": config["version"], "results": results}
    print(json.dumps(out, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
