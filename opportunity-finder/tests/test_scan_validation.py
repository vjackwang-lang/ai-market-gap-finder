import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_scan.py"
spec = importlib.util.spec_from_file_location("validate_scan", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
CONFIG = json.loads((ROOT / "config" / "criteria.json").read_text(encoding="utf-8"))


def ev(url="https://example.com/post", date="2026-08-26"):
    return {
        "claim_type": "demand",
        "source_type": "forum",
        "source_reference": url,
        "source_date": date,
        "observed_at": "2026-08-26",
    }


def winner(url="https://example.com/winner"):
    return {
        "product_name": "winner",
        "source_reference": url,
        "observation_date": "2026-08-26",
        "job_to_be_done": "find a specialized skill",
        "signal_quality_notes": "standalone listing; install count treated as exposure only",
        "adjacent_unresolved_job": "verify whether discovered skills are still worth installing",
    }


class ScanValidationTests(unittest.TestCase):
    def scored(self, names, decisions):
        return {"results": [{"name": n, "decision": d} for n, d in zip(names, decisions)]}

    def broad(self, domains):
        return {
            "scan_scope": "broad",
            "winner_benchmarks": [winner()],
            "candidates": [
                {"name": f"c{i}", "domain": d, "evidence": [ev(f"https://example.com/{i}")]}
                for i, d in enumerate(domains)
            ],
        }

    def test_broad_scan_needs_minimum_domains(self):
        candidates = self.broad(["core-agent-dev", "research-knowledge"])
        out = mod.validate(candidates, self.scored(["c0", "c1"], ["SKIP", "SKIP"]), CONFIG)
        self.assertFalse(out["scan_complete"])

    def test_broad_scan_with_diverse_domains_and_sources_can_finish_zero_ship(self):
        domains = ["core-agent-dev", "research-knowledge", "design-3d-cad", "office-data", "automation-ops"]
        candidates = self.broad(domains)
        out = mod.validate(candidates, self.scored([f"c{i}" for i in range(5)], ["SKIP"]*5), CONFIG)
        self.assertTrue(out["scan_complete"])
        self.assertEqual(out["ship_count"], 0)
        self.assertEqual(out["traceable_winner_benchmark_count"], 1)
        self.assertEqual(out["traceable_candidate_ratio"], 1.0)

    def test_broad_scan_requires_traceable_winner_benchmark(self):
        domains = ["core-agent-dev", "research-knowledge", "design-3d-cad", "office-data", "automation-ops"]
        candidates = self.broad(domains)
        candidates["winner_benchmarks"] = []
        out = mod.validate(candidates, self.scored([f"c{i}" for i in range(5)], ["SKIP"]*5), CONFIG)
        self.assertFalse(out["scan_complete"])
        self.assertTrue(any("Winner Benchmarks" in r for r in out["incomplete_reasons"]))

    def test_broad_scan_requires_original_source_url_and_observation_date(self):
        domains = ["core-agent-dev", "research-knowledge", "design-3d-cad", "office-data", "automation-ops"]
        candidates = self.broad(domains)
        candidates["candidates"][2]["evidence"] = [{"source_reference": "reddit post", "observed_at": "2026-08-26"}]
        out = mod.validate(candidates, self.scored([f"c{i}" for i in range(5)], ["SKIP"]*5), CONFIG)
        self.assertFalse(out["scan_complete"])
        self.assertLess(out["traceable_candidate_ratio"], 1.0)

    def test_winner_requires_adjacent_unresolved_job(self):
        domains = ["core-agent-dev", "research-knowledge", "design-3d-cad", "office-data", "automation-ops"]
        candidates = self.broad(domains)
        candidates["winner_benchmarks"][0]["adjacent_unresolved_job"] = ""
        out = mod.validate(candidates, self.scored([f"c{i}" for i in range(5)], ["SKIP"]*5), CONFIG)
        self.assertFalse(out["scan_complete"])

    def test_narrow_scan_does_not_require_domain_or_winner_diversity(self):
        candidates = {"scan_scope": "narrow", "candidates": [
            {"name": "a", "domain": "core-agent-dev"},
        ]}
        out = mod.validate(candidates, self.scored(["a"], ["SKIP"]), CONFIG)
        self.assertTrue(out["scan_complete"])


if __name__ == "__main__":
    unittest.main()
