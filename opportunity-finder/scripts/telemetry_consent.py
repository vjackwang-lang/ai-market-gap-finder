#!/usr/bin/env python3
"""Manage local Opportunity Finder telemetry consent.

Consent is stored only on the user's machine at ~/.opportunity-finder/telemetry.json
(or OPPORTUNITY_FINDER_HOME when set). Declining does not reduce Skill features.
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

USER_HOME_ENV = "OPPORTUNITY_FINDER_HOME"
VALID_PLATFORMS = {"unknown", "workbuddy", "claude-code", "codex", "cursor", "openclaw", "gemini-cli", "other"}


def data_dir() -> Path:
    override = os.environ.get(USER_HOME_ENV, "").strip()
    if override:
        return Path(override).expanduser()
    return Path.home() / ".opportunity-finder"


def state_path() -> Path:
    return data_dir() / "telemetry.json"


def read_state() -> dict:
    path = state_path()
    if not path.exists():
        return {"consent_state": "unknown", "enabled": False, "platform": "unknown"}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"consent_state": "unknown", "enabled": False, "platform": "unknown"}
    return {
        "consent_state": str(state.get("consent_state", "unknown")),
        "enabled": bool(state.get("enabled", False)),
        "platform": str(state.get("platform", "unknown")),
        "updated_at": state.get("updated_at"),
    }


def write_state(consent: str, platform: str) -> dict:
    if platform not in VALID_PLATFORMS:
        platform = "other"
    directory = data_dir(); directory.mkdir(parents=True, exist_ok=True)
    state = {
        "consent_state": consent,
        "enabled": consent == "yes",
        "platform": platform,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    state_path().write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return state


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage anonymous telemetry consent")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    enable = sub.add_parser("enable"); enable.add_argument("--platform", default="unknown")
    disable = sub.add_parser("disable"); disable.add_argument("--platform", default="unknown")
    args = parser.parse_args()
    if args.command == "status":
        result = read_state()
    elif args.command == "enable":
        result = write_state("yes", args.platform)
    else:
        result = write_state("no", args.platform)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
