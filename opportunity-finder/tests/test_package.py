import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_required_files_exist(self):
        required = [
            "SKILL.md",
            "README.md",
            "CHANGELOG.md",
            "LICENSE.txt",
            "QA_REPORT.md",
            "HOST_COMPAT_REPORT.md",
            "config/criteria.json",
            "config/telemetry.defaults.json",
            "config/telemetry.example.json",
            "POSTHOG_SETUP.md",
            "scripts/score_opportunities.py",
            "scripts/validate_scan.py",
            "scripts/telemetry_client.py",
            "scripts/telemetry_consent.py",
            "scripts/local_ledger.py",
            "scripts/render_source_ledger.py",
            "references/business-model.md",
            "references/telemetry-policy.md",
            "references/winner-benchmark.md",
            "references/winner-patterns.md",
            "references/signal-hierarchy.md",
            "references/competitor-map.md",
            "references/feasibility-gates.md",
            "references/competition-maturity.md",
            "references/platform-incident-quarantine.md",
            "references/source-traceability.md",
            "PRIVACY.md",
            "MARKETPLACE_LISTING.md",
            "DEMO.md",
            "PUBLISH_CHECKLIST.md",
            "LIVE_HOST_ACCEPTANCE.md",
            "SPEC_VALIDATION.md",
            "assets/icon.svg",
            "assets/cover.svg",
            "assets/icon.png",
            "assets/cover.png",
        ]
        for rel in required:
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_skill_frontmatter_and_version(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        self.assertRegex(text, r"(?m)^name: opportunity-finder$")
        self.assertRegex(text, r'(?m)^  version: "1\.6\.2"$')
        self.assertLess(len(text.splitlines()), 500)

    def test_official_telemetry_defaults_use_public_posthog_project_token(self):
        cfg = json.loads((ROOT / "config/telemetry.defaults.json").read_text(encoding="utf-8"))
        self.assertEqual(cfg["posthog_host"], "https://us.i.posthog.com")
        self.assertTrue(cfg["posthog_project_api_key"].startswith("phc_"))
        self.assertNotIn("enabled", cfg)

    def test_no_consent_state_is_packaged(self):
        self.assertFalse((ROOT / "config/telemetry.json").exists())
        self.assertFalse((ROOT / ".opportunity-finder").exists())

    def test_telemetry_template_version_matches_skill(self):
        cfg = json.loads((ROOT / "config/telemetry.defaults.json").read_text(encoding="utf-8"))
        self.assertEqual(cfg["skill_version"], "1.6.2")

    def test_telemetry_client_uses_publisher_release_version(self):
        text = (ROOT / "scripts/telemetry_client.py").read_text(encoding="utf-8")
        self.assertIn('payload["skill_version"] = str(config.get("skill_version", "unknown"))', text)
        self.assertNotIn('payload.get("skill_version") or config.get("skill_version"', text)

    def test_public_readme_is_not_release_candidate(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Public Free Release", text)
        self.assertNotIn("Traceable Winner-Benchmark RC", text)

    def test_source_output_requires_full_clickable_urls(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        ref = (ROOT / "references/source-traceability.md").read_text(encoding="utf-8")
        self.assertIn("never strip the URL scheme", skill)
        self.assertIn("clickable Markdown link", ref)


    def test_parent_directory_matches_frontmatter_name(self):
        skill = ROOT / "SKILL.md"
        text = skill.read_text(encoding="utf-8")
        import re
        m = re.search(r"^name:\s*([^\n]+)$", text, re.MULTILINE)
        self.assertIsNotNone(m)
        self.assertEqual(ROOT.name, m.group(1).strip().strip('"\''))

    def test_agent_skills_frontmatter_shape(self):
        skill = ROOT / "SKILL.md"
        text = skill.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---", 2)[1]
        allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
        top = []
        for line in frontmatter.splitlines():
            if not line or line.startswith(" ") or line.startswith("\t") or line.startswith("#"):
                continue
            if ":" in line:
                top.append(line.split(":", 1)[0].strip())
        self.assertTrue(set(top).issubset(allowed), (set(top) - allowed))
        self.assertLessEqual(len(text.splitlines()), 500)

    def test_public_traceability_and_winner_gates_are_present(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Source Ledger", text)
        self.assertIn("traceable Winner Benchmarks", text)
        self.assertTrue((ROOT / "references/source-traceability.md").is_file())

if __name__ == "__main__":
    unittest.main()
