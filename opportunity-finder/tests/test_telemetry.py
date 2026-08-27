import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
CLIENT = ROOT / "scripts" / "telemetry_client.py"
CONSENT = ROOT / "scripts" / "telemetry_consent.py"

spec = importlib.util.spec_from_file_location("telemetry_client", CLIENT)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
spec2 = importlib.util.spec_from_file_location("telemetry_consent", CONSENT)
consent = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(consent)


class TelemetryTests(unittest.TestCase):
    def base_config(self):
        return {
            "enabled": True,
            "consent_state": "yes",
            "provider": "posthog",
            "posthog_host": "https://us.i.posthog.com",
            "posthog_project_api_key": "phc_test_public_project_key",
            "platform": "workbuddy",
            "skill_version": "1.6.2",
            "timeout_seconds": 1,
            "telemetry_schema_version": "1",
        }

    def event(self):
        return {
            "event": "scan_completed", "mode": "quick-commerce", "coarse_category": "agent-tools", "time_window": "7d",
            "result_ship_count": 0, "result_test_count": 1, "result_watch_count": 2, "result_skip_count": 7,
        }

    def test_no_consent_fails_closed(self):
        c = self.base_config(); c.update({"enabled": False, "consent_state": "unknown"})
        self.assertEqual(mod.send_event(self.event(), c)["reason"], "disabled_or_no_consent")

    def test_explicit_no_fails_closed(self):
        c = self.base_config(); c.update({"enabled": False, "consent_state": "no"})
        self.assertEqual(mod.send_event(self.event(), c)["reason"], "disabled_or_no_consent")

    def test_missing_posthog_key_fails_closed(self):
        c = self.base_config(); c["posthog_project_api_key"] = ""
        with tempfile.TemporaryDirectory() as td:
            result = mod.send_event(self.event(), c, base_dir=Path(td))
        self.assertEqual(result["reason"], "missing_posthog_project_api_key")

    def test_unknown_field_rejected(self):
        c = self.base_config(); e = self.event(); e["prompt"] = "secret"
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError): mod.send_event(e, c, base_dir=Path(td))

    def test_unsupported_event_rejected(self):
        c = self.base_config(); e = self.event(); e["event"] = "raw_prompt"
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError): mod.send_event(e, c, base_dir=Path(td))

    def test_posthog_payload_shape_and_no_person_profile(self):
        c = self.base_config(); sent = []
        with tempfile.TemporaryDirectory() as td:
            result = mod.send_event(self.event(), c, transport=lambda endpoint, body, timeout: sent.append((endpoint, json.loads(body), timeout)), base_dir=Path(td))
        self.assertTrue(result["sent"])
        endpoint, body, _ = sent[0]
        self.assertEqual(endpoint, "https://us.i.posthog.com/i/v0/e/")
        self.assertEqual(body["event"], "opportunity_finder_scan_completed")
        self.assertTrue(body["api_key"].startswith("phc_"))
        self.assertFalse(body["properties"]["$process_person_profile"])
        self.assertTrue(body["properties"]["$geoip_disable"])
        self.assertNotIn("anonymous_id", body["properties"])
        self.assertNotIn("prompt", json.dumps(body))

    def test_agent_supplied_skill_version_cannot_override_release_version(self):
        c = self.base_config(); e = self.event(); e["skill_version"] = "1.6.1"
        sent = []
        with tempfile.TemporaryDirectory() as td:
            result = mod.send_event(e, c, transport=lambda endpoint, body, timeout: sent.append(json.loads(body)), base_dir=Path(td))
        self.assertTrue(result["sent"])
        self.assertEqual(sent[0]["properties"]["skill_version"], "1.6.2")

    def test_duplicate_scan_completed_is_suppressed_locally(self):
        c = self.base_config(); sent = []
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            first = mod.send_event(self.event(), c, transport=lambda endpoint, body, timeout: sent.append(json.loads(body)), base_dir=base)
            second = mod.send_event(self.event(), c, transport=lambda endpoint, body, timeout: sent.append(json.loads(body)), base_dir=base)
        self.assertTrue(first["sent"])
        self.assertFalse(second["sent"])
        self.assertEqual(second["reason"], "duplicate_suppressed")
        self.assertEqual(len(sent), 1)

    def test_failed_send_is_not_recorded_as_duplicate(self):
        c = self.base_config()
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            failed = mod.send_event(self.event(), c, transport=lambda *args: (_ for _ in ()).throw(OSError("offline")), base_dir=base)
            sent = []
            retry = mod.send_event(self.event(), c, transport=lambda endpoint, body, timeout: sent.append(json.loads(body)), base_dir=base)
        self.assertEqual(failed["reason"], "network_error")
        self.assertTrue(retry["sent"])
        self.assertEqual(len(sent), 1)

    def test_feedback_events_are_not_deduplicated(self):
        c = self.base_config(); e = {"event": "feedback", "feedback_value": "helpful"}; sent = []
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            first = mod.send_event(e, c, transport=lambda endpoint, body, timeout: sent.append(json.loads(body)), base_dir=base)
            second = mod.send_event(e, c, transport=lambda endpoint, body, timeout: sent.append(json.loads(body)), base_dir=base)
        self.assertTrue(first["sent"]); self.assertTrue(second["sent"]); self.assertEqual(len(sent), 2)

    def test_network_failure_never_breaks_skill(self):
        c = self.base_config()
        def boom(*args): raise OSError("offline")
        with tempfile.TemporaryDirectory() as td:
            result = mod.send_event(self.event(), c, transport=boom, base_dir=Path(td))
        self.assertFalse(result["sent"]); self.assertEqual(result["reason"], "network_error")

    def test_anonymous_id_persists_locally(self):
        c = self.base_config()
        with tempfile.TemporaryDirectory() as td:
            base = Path(td); a = mod.get_or_create_anonymous_id(c, base); b = mod.get_or_create_anonymous_id(c, base)
        self.assertEqual(a, b)

    def test_local_consent_enable_disable(self):
        with tempfile.TemporaryDirectory() as td, mock.patch.dict(os.environ, {"OPPORTUNITY_FINDER_HOME": td}):
            self.assertEqual(consent.read_state()["consent_state"], "unknown")
            consent.write_state("yes", "workbuddy"); self.assertTrue(consent.read_state()["enabled"])
            consent.write_state("no", "workbuddy"); self.assertFalse(consent.read_state()["enabled"])

    def test_load_config_requires_local_consent(self):
        with tempfile.TemporaryDirectory() as td:
            c = mod.load_config(base_dir=Path(td)); self.assertFalse(c["enabled"]); self.assertEqual(c["consent_state"], "unknown")
            Path(td, "telemetry.json").write_text(json.dumps({"consent_state":"yes","enabled":True,"platform":"workbuddy"}), encoding="utf-8")
            c = mod.load_config(base_dir=Path(td)); self.assertTrue(c["enabled"]); self.assertEqual(c["platform"], "workbuddy")


if __name__ == "__main__": unittest.main()
