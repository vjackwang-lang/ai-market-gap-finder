import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "local_ledger.py"
spec = importlib.util.spec_from_file_location("local_ledger", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class LedgerTests(unittest.TestCase):
    def test_append_and_summary(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "history.jsonl"
            mod.append_record(path, {
                "event": "candidate", "candidate_id": "x1", "decision": "SHIP",
                "portfolio_role": "PAID_UTILITY", "suggested_price_usd": 9.99,
                "build_hours": 4, "coarse_category": "research"
            })
            mod.append_record(path, {
                "event": "outcome", "candidate_id": "x1", "paid_sales": 3,
                "revenue_usd": 29.97, "status": "GROW"
            })
            records = mod.read_records(path)
            summary = mod.summarize(records)
        self.assertEqual(summary["records"], 2)
        self.assertEqual(summary["decisions"]["SHIP"], 1)
        self.assertEqual(summary["paid_sales_total"], 3.0)
        self.assertEqual(summary["revenue_usd_total"], 29.97)

    def test_rejects_arbitrary_private_text_field(self):
        with self.assertRaises(ValueError):
            mod.sanitize({"event": "candidate", "prompt": "private"})


if __name__ == "__main__":
    unittest.main()
