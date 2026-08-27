import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_source_ledger.py"
spec = importlib.util.spec_from_file_location("render_source_ledger", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class SourceRendererTests(unittest.TestCase):
    def test_renderer_preserves_clickable_full_scheme_links(self):
        scan = {
            "winner_benchmarks": [{
                "product": "winner",
                "source_reference": "https://example.com/winner",
                "observed_at": "2026-08-26",
                "job_to_be_done": "do the job",
            }],
            "candidates": [{
                "name": "candidate",
                "evidence": [{
                    "claim_type": "competition",
                    "source_reference": "https://github.com/example/repo/issues/1",
                    "observed_at": "2026-08-26",
                    "note": "existing alternative",
                }],
            }],
        }
        text = mod.render(mod.collect(scan))
        self.assertIn("[example.com](https://example.com/winner)", text)
        self.assertIn("[github.com](https://github.com/example/repo/issues/1)", text)
        self.assertNotIn("](example.com/", text)

    def test_non_http_sources_are_ignored(self):
        scan = {"candidates": [{"name": "x", "evidence": [{"source_reference": "reddit.com/no-scheme"}]}]}
        rows = mod.collect(scan)
        self.assertEqual(rows, [])


if __name__ == "__main__":
    unittest.main()
