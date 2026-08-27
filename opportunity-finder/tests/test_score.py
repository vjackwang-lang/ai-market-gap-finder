import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "score_opportunities.py"
spec = importlib.util.spec_from_file_location("score_opportunities", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
CONFIG = json.loads((ROOT / "config" / "criteria.json").read_text(encoding="utf-8"))


class ScoreTests(unittest.TestCase):
    def base_candidate(self):
        return {
            "name": "test",
            "evidence_count": 3,
            "evidence": [
                {"source_reference": "https://example.com/a", "observed_at": "2026-08-26"},
                {"source_reference": "https://example.com/b", "observed_at": "2026-08-26"},
                {"source_reference": "https://example.com/c", "observed_at": "2026-08-26"},
            ],
            "scores": {key: 10 for key in CONFIG["weights"]},
            "flags": {},
            "economics": {
                "build_hours": 4,
                "cash_cost_usd": 0,
                "internal_hourly_rate_usd": 25,
                "suggested_price_usd": 10,
                "platform_fee_pct": 20,
                "variable_cost_per_paid_user_usd": 0,
                "runtime_model_cost_owner": "user",
                "portfolio_role": "PAID_UTILITY",
            },
            "implementation": {
                "build_estimate_confidence": 0.9,
                "required_surfaces": ["local-files"],
                "stable_interfaces": ["filesystem"],
                "test_path": "fixture-based local test",
                "workaround_minutes": 30,
                "surface_accessible": True,
                "implementation_path_verified": True,
            },
        }

    def test_weights_sum_to_100(self):
        self.assertEqual(sum(CONFIG["weights"].values()), 100)

    def test_perfect_candidate_ships(self):
        result = mod.score_candidate(self.base_candidate(), CONFIG)
        self.assertEqual(result["weighted_score"], 100.0)
        self.assertEqual(result["decision"], "SHIP")

    def test_low_evidence_count_caps_ship_to_test(self):
        c = self.base_candidate()
        c["evidence_count"] = 1
        result = mod.score_candidate(c, CONFIG)
        self.assertEqual(result["decision"], "TEST")

    def test_untraceable_evidence_cannot_ship(self):
        c = self.base_candidate()
        c["evidence"] = [{"source_reference": "reddit summary", "observed_at": "2026-08-26"}]
        result = mod.score_candidate(c, CONFIG)
        self.assertGreaterEqual(result["weighted_score"], CONFIG["decision_bands"]["ship"])
        self.assertEqual(result["decision"], "TEST")
        self.assertEqual(result["evidence_traceability"]["traceable_original_source_count"], 0)

    def test_low_evidence_quality_caps_ship_to_test(self):
        c = self.base_candidate()
        c["scores"]["evidence_quality"] = 5.5
        result = mod.score_candidate(c, CONFIG)
        self.assertGreaterEqual(result["weighted_score"], CONFIG["decision_bands"]["ship"])
        self.assertEqual(result["decision"], "TEST")

    def test_platform_capture_is_penalty_not_hard_reject(self):
        c = self.base_candidate()
        c["flags"]["platform_capture_soon"] = True
        result = mod.score_candidate(c, CONFIG)
        self.assertEqual(result["weighted_score"], 95.0)
        self.assertEqual(result["decision"], "SHIP")

    def test_hard_reject_overrides_score(self):
        c = self.base_candidate()
        c["flags"]["no_current_demand_evidence"] = True
        result = mod.score_candidate(c, CONFIG)
        self.assertEqual(result["decision"], "SKIP")

    def test_build_hours_auto_skip(self):
        c = self.base_candidate()
        c["economics"]["build_hours"] = 30
        result = mod.score_candidate(c, CONFIG)
        self.assertEqual(result["decision"], "SKIP")
        self.assertIn("build_over_hard_limit", result["hard_reject_reasons"])

    def test_legacy_build_flag_still_skips(self):
        c = self.base_candidate()
        c["flags"]["build_over_3_days"] = True
        result = mod.score_candidate(c, CONFIG)
        self.assertEqual(result["decision"], "SKIP")

    def test_economics_break_even(self):
        c = self.base_candidate()
        result = mod.score_candidate(c, CONFIG)
        econ = result["economics_summary"]
        self.assertEqual(econ["estimated_dev_cost_usd"], 100.0)
        self.assertEqual(econ["net_revenue_per_sale_usd"], 8.0)
        self.assertEqual(econ["breakeven_paid_users"], 13)

    def test_free_anchor_without_asset_is_penalized(self):
        c = self.base_candidate()
        c["economics"]["suggested_price_usd"] = 0
        c["economics"]["portfolio_role"] = "FREE_ANCHOR"
        result = mod.score_candidate(c, CONFIG)
        self.assertIn("free_without_asset", result["penalties_applied"])
        self.assertEqual(result["weighted_score"], 85.0)

    def test_free_anchor_with_asset_not_penalized(self):
        c = self.base_candidate()
        c["economics"]["suggested_price_usd"] = 0
        c["economics"]["portfolio_role"] = "FREE_ANCHOR"
        c["free_asset_targets"] = ["installs", "opt_in_telemetry"]
        result = mod.score_candidate(c, CONFIG)
        self.assertNotIn("free_without_asset", result["penalties_applied"])
        self.assertIsNone(result["economics_summary"]["breakeven_paid_users"])
        self.assertEqual(result["decision"], "SHIP")

    def test_ambiguous_install_signal_penalty(self):
        c = self.base_candidate()
        c["flags"]["ambiguous_install_signal"] = True
        result = mod.score_candidate(c, CONFIG)
        self.assertEqual(result["weighted_score"], 95.0)
        self.assertIn("ambiguous_install_signal", result["penalties_applied"])

    def test_seller_paid_runtime_penalty(self):
        c = self.base_candidate()
        c["flags"]["seller_paid_runtime"] = True
        c["economics"]["runtime_model_cost_owner"] = "seller"
        result = mod.score_candidate(c, CONFIG)
        self.assertEqual(result["weighted_score"], 90.0)
        self.assertIn("seller_paid_runtime", result["penalties_applied"])


    def test_low_technical_feasibility_caps_ship_to_test(self):
        c = self.base_candidate()
        c["scores"]["technical_feasibility"] = 6.5
        result = mod.score_candidate(c, CONFIG)
        self.assertGreaterEqual(result["weighted_score"], CONFIG["decision_bands"]["ship"])
        self.assertEqual(result["decision"], "TEST")

    def test_low_workaround_friction_caps_ship_to_test(self):
        c = self.base_candidate()
        c["scores"]["workaround_friction"] = 5.0
        result = mod.score_candidate(c, CONFIG)
        self.assertGreaterEqual(result["weighted_score"], CONFIG["decision_bands"]["ship"])
        self.assertEqual(result["decision"], "TEST")

    def test_low_build_estimate_confidence_caps_ship_to_test(self):
        c = self.base_candidate()
        c["implementation"]["build_estimate_confidence"] = 0.5
        result = mod.score_candidate(c, CONFIG)
        self.assertEqual(result["decision"], "TEST")

    def test_inaccessible_surface_hard_rejects(self):
        c = self.base_candidate()
        c["flags"]["inaccessible_required_surface"] = True
        result = mod.score_candidate(c, CONFIG)
        self.assertEqual(result["decision"], "SKIP")
        self.assertIn("inaccessible_required_surface", result["hard_reject_reasons"])

    def test_trivial_workaround_penalty(self):
        c = self.base_candidate()
        c["flags"]["trivial_workaround"] = True
        result = mod.score_candidate(c, CONFIG)
        self.assertEqual(result["weighted_score"], 80.0)
        self.assertIn("trivial_workaround", result["penalties_applied"])

    def test_missing_implementation_cannot_ship(self):
        c = self.base_candidate()
        c.pop("implementation")
        result = mod.score_candidate(c, CONFIG)
        self.assertNotEqual(result["decision"], "SHIP")
        self.assertIn("low_build_estimate_confidence", result["penalties_applied"])

    def test_workaround_minutes_auto_penalty(self):
        c = self.base_candidate()
        c["implementation"]["workaround_minutes"] = 2
        result = mod.score_candidate(c, CONFIG)
        self.assertIn("trivial_workaround", result["penalties_applied"])

    def test_explicit_inaccessible_surface_auto_rejects(self):
        c = self.base_candidate()
        c["implementation"]["surface_accessible"] = False
        result = mod.score_candidate(c, CONFIG)
        self.assertEqual(result["decision"], "SKIP")

    def test_unverified_path_caps_ship(self):
        c = self.base_candidate()
        c["implementation"]["implementation_path_verified"] = None
        result = mod.score_candidate(c, CONFIG)
        self.assertEqual(result["decision"], "TEST")


    def test_emerging_free_alternatives_get_small_penalty(self):
        c = self.base_candidate()
        c["competition"] = {"maturity": "emerging"}
        result = mod.score_candidate(c, CONFIG)
        self.assertEqual(result["weighted_score"], 94.0)
        self.assertIn("emerging_free_alternatives", result["penalties_applied"])
        self.assertNotIn("mature_free_incumbent", result["penalties_applied"])

    def test_mature_competition_auto_penalizes(self):
        c = self.base_candidate()
        c["competition"] = {"maturity": "mature"}
        result = mod.score_candidate(c, CONFIG)
        self.assertEqual(result["weighted_score"], 80.0)
        self.assertIn("mature_free_incumbent", result["penalties_applied"])

    def test_platform_incident_root_cause_hard_rejects(self):
        c = self.base_candidate()
        c["root_cause"] = {"platform_incident_only": True, "user_controlled_fix": False}
        result = mod.score_candidate(c, CONFIG)
        self.assertEqual(result["decision"], "SKIP")
        self.assertIn("platform_incident_only", result["hard_reject_reasons"])

    def test_invalid_competition_maturity_raises(self):
        c = self.base_candidate()
        c["competition"] = {"maturity": "kind-of"}
        with self.assertRaises(ValueError):
            mod.score_candidate(c, CONFIG)

    def test_invalid_score_raises(self):
        c = self.base_candidate()
        c["scores"]["freshness"] = 11
        with self.assertRaises(ValueError):
            mod.score_candidate(c, CONFIG)


if __name__ == "__main__":
    unittest.main()
