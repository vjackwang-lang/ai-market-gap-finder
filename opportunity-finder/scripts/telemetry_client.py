#!/usr/bin/env python3
"""Privacy-first optional telemetry client for Opportunity Finder.

Telemetry is fail-closed and requires an explicit local opt-in state written by
telemetry_consent.py. The public PostHog project token identifies the ingestion
project; it is not a personal/admin API secret.

The client transmits only a strict allowlist of coarse product-usage fields.
It never accepts prompts, URLs, file contents, API keys, reports, company names,
emails, private repository names, or arbitrary free text.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
import uuid
from pathlib import Path
from urllib import request

ROOT = Path(__file__).resolve().parents[1]
DEFAULTS_CONFIG = ROOT / "config" / "telemetry.defaults.json"
USER_HOME_ENV = "OPPORTUNITY_FINDER_HOME"

ALLOWED_EVENTS = {
    "scan_completed",
    "winner_benchmark_completed",
    "event_radar_completed",
    "candidate_action",
    "feedback",
}
ALLOWED_FIELDS = {
    "event",
    "platform",
    "skill_version",
    "mode",
    "coarse_category",
    "time_window",
    "result_ship_count",
    "result_test_count",
    "result_watch_count",
    "result_skip_count",
    "action",
    "portfolio_role",
    "feedback_value",
}


def user_data_dir(base_dir: Path | None = None) -> Path:
    if base_dir is not None:
        return Path(base_dir)
    override = os.environ.get(USER_HOME_ENV, "").strip()
    if override:
        return Path(override).expanduser()
    return Path.home() / ".opportunity-finder"


def consent_path(base_dir: Path | None = None) -> Path:
    return user_data_dir(base_dir) / "telemetry.json"


DEDUPE_EVENTS = {"scan_completed", "winner_benchmark_completed", "event_radar_completed"}
DEDUPE_WINDOW_SECONDS = 180


def dedupe_path(base_dir: Path | None = None) -> Path:
    return user_data_dir(base_dir) / "telemetry_dedupe.json"


def _dedupe_fingerprint(payload: dict) -> str:
    stable = {k: payload[k] for k in sorted(payload) if k != "anonymous_id"}
    raw = json.dumps(stable, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def is_recent_duplicate(payload: dict, base_dir: Path | None = None, now: float | None = None) -> bool:
    if payload.get("event") not in DEDUPE_EVENTS:
        return False
    path = dedupe_path(base_dir)
    try:
        state = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    except Exception:
        return False
    fp = _dedupe_fingerprint(payload)
    record = state.get(fp)
    if not isinstance(record, dict):
        return False
    ts = record.get("sent_at")
    if not isinstance(ts, (int, float)):
        return False
    return (float(now if now is not None else time.time()) - float(ts)) < DEDUPE_WINDOW_SECONDS


def record_sent_event(payload: dict, base_dir: Path | None = None, now: float | None = None) -> None:
    if payload.get("event") not in DEDUPE_EVENTS:
        return
    directory = user_data_dir(base_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = dedupe_path(base_dir)
    try:
        state = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    except Exception:
        state = {}
    current = float(now if now is not None else time.time())
    cutoff = current - max(DEDUPE_WINDOW_SECONDS * 10, 3600)
    cleaned = {}
    for key, value in state.items():
        if isinstance(value, dict) and isinstance(value.get("sent_at"), (int, float)) and float(value["sent_at"]) >= cutoff:
            cleaned[key] = value
    cleaned[_dedupe_fingerprint(payload)] = {"sent_at": current}
    path.write_text(json.dumps(cleaned, separators=(",", ":")), encoding="utf-8")


def load_config(path: Path | None = None, base_dir: Path | None = None) -> dict:
    defaults_path = path or DEFAULTS_CONFIG
    defaults = json.loads(defaults_path.read_text(encoding="utf-8"))
    state_path = consent_path(base_dir)
    if not state_path.exists():
        defaults["enabled"] = False
        defaults["consent_state"] = "unknown"
        return defaults
    state = json.loads(state_path.read_text(encoding="utf-8"))
    # Only local consent/preferences may override these fields. The destination
    # and project token remain publisher-controlled defaults.
    defaults["enabled"] = bool(state.get("enabled", False))
    defaults["consent_state"] = str(state.get("consent_state", "unknown"))
    if state.get("platform"):
        defaults["platform"] = str(state["platform"])
    return defaults


def get_or_create_anonymous_id(config: dict, base_dir: Path | None = None) -> str:
    directory = user_data_dir(base_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "anonymous_id"
    if path.exists():
        value = path.read_text(encoding="utf-8").strip()
        if value:
            return value
    value = str(uuid.uuid4())
    path.write_text(value, encoding="utf-8")
    return value


def sanitize_event(event: dict, config: dict, anonymous_id: str) -> dict:
    if not isinstance(event, dict):
        raise ValueError("event must be a JSON object")
    unknown = set(event) - ALLOWED_FIELDS
    if unknown:
        raise ValueError(f"telemetry contains non-allowlisted fields: {', '.join(sorted(unknown))}")
    event_name = event.get("event")
    if event_name not in ALLOWED_EVENTS:
        raise ValueError(f"unsupported telemetry event: {event_name}")
    payload = {k: event[k] for k in event if k in ALLOWED_FIELDS}
    payload["anonymous_id"] = anonymous_id
    payload["platform"] = str(payload.get("platform") or config.get("platform", "unknown"))
    # Release version is publisher-controlled. Ignore any agent-supplied value so
    # the scoring-criteria version cannot accidentally masquerade as Skill version.
    payload["skill_version"] = str(config.get("skill_version", "unknown"))
    return payload


def _post_json(endpoint: str, body: bytes, timeout: float, transport=None) -> None:
    if transport is not None:
        transport(endpoint, body, timeout)
        return
    req = request.Request(endpoint, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with request.urlopen(req, timeout=timeout) as resp:
        resp.read(1)


def _build_posthog_request(payload: dict, config: dict) -> tuple[str, bytes]:
    host = str(config.get("posthog_host", "")).strip().rstrip("/")
    project_key = str(config.get("posthog_project_api_key", "")).strip()
    if not project_key:
        raise ValueError("missing_posthog_project_api_key")
    if not project_key.startswith("phc_"):
        raise ValueError("invalid_posthog_project_api_key")
    if not host.startswith("https://"):
        raise ValueError("posthog_host_must_use_https")
    event_name = str(payload["event"])
    properties = {k: v for k, v in payload.items() if k not in {"event", "anonymous_id"}}
    properties["telemetry_schema_version"] = str(config.get("telemetry_schema_version", "1"))
    properties["$process_person_profile"] = False
    # Disable PostHog GeoIP enrichment so opted-in coarse telemetry does not
    # acquire derived city/country/coordinate properties from the request IP.
    properties["$geoip_disable"] = True
    body = {
        "api_key": project_key,
        "event": f"opportunity_finder_{event_name}",
        "distinct_id": payload["anonymous_id"],
        "properties": properties,
    }
    return f"{host}/i/v0/e/", json.dumps(body, separators=(",", ":")).encode("utf-8")


def _build_generic_request(payload: dict, config: dict) -> tuple[str, bytes]:
    endpoint = str(config.get("endpoint", "")).strip()
    if not endpoint:
        raise ValueError("missing_endpoint")
    if not endpoint.startswith("https://"):
        raise ValueError("telemetry_endpoint_must_use_https")
    return endpoint, json.dumps(payload, separators=(",", ":")).encode("utf-8")


def send_event(event: dict, config: dict | None = None, transport=None, base_dir: Path | None = None) -> dict:
    config = config or load_config(base_dir=base_dir)
    if not bool(config.get("enabled", False)):
        return {"sent": False, "reason": "disabled_or_no_consent"}
    if str(config.get("consent_state", "yes")) != "yes":
        return {"sent": False, "reason": "disabled_or_no_consent"}
    anonymous_id = get_or_create_anonymous_id(config, base_dir=base_dir)
    payload = sanitize_event(event, config, anonymous_id)
    if is_recent_duplicate(payload, base_dir=base_dir):
        return {"sent": False, "reason": "duplicate_suppressed"}
    provider = str(config.get("provider", "generic")).strip().lower()
    try:
        if provider == "posthog":
            endpoint, body = _build_posthog_request(payload, config)
        elif provider == "generic":
            endpoint, body = _build_generic_request(payload, config)
        else:
            return {"sent": False, "reason": "unsupported_provider"}
    except ValueError as exc:
        return {"sent": False, "reason": str(exc)}
    timeout = float(config.get("timeout_seconds", 3))
    try:
        _post_json(endpoint, body, timeout, transport=transport)
    except Exception as exc:
        # Telemetry must never break the core Skill workflow.
        return {"sent": False, "reason": "network_error", "error_type": type(exc).__name__}
    try:
        record_sent_event(payload, base_dir=base_dir)
    except Exception:
        # Local dedupe bookkeeping is analytics-only and must never break the Skill.
        pass
    return {"sent": True, "provider": provider, "payload": payload}


def main() -> int:
    parser = argparse.ArgumentParser(description="Send one optional anonymous Opportunity Finder telemetry event")
    parser.add_argument("event_json", type=Path)
    parser.add_argument("--config", type=Path, default=None, help="Override publisher defaults (QA/forks only)")
    args = parser.parse_args()
    config = load_config(args.config)
    event = json.loads(args.event_json.read_text(encoding="utf-8"))
    result = send_event(event, config)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
