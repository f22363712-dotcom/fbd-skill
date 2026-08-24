import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_english.py"
SPEC = importlib.util.spec_from_file_location("check_english", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class CheckEnglishTests(unittest.TestCase):
    def test_dense_correction_reply_fails(self):
        draft = (
            "One nuance: a ±6.1% implied move is a snapshot, so it changes with expiry and timing. "
            "Even if all eight closes landed inside the range, that doesn't prove an easy short-vol trade. "
            "Entry IV, strikes, spreads and exit timing still decide whether the trade worked."
        )
        result = MODULE.inspect(draft, "reply", 280)
        codes = {issue["code"] for issue in result["failures"]}
        self.assertFalse(result["ok"])
        self.assertIn("stock_opener", codes)
        self.assertIn("jargon_stack", codes)

    def test_human_peer_reply_passes_deterministic_checks(self):
        draft = (
            "That 8-for-8 stat is interesting. Which expiry and timestamp did you use for the 6.1% move? "
            "Landing inside the range still leaves the entry price and spread to check."
        )
        result = MODULE.inspect(draft, "reply", 280)
        self.assertTrue(result["ok"], result)

    def test_repeated_opener_fails_with_history(self):
        draft = "The demand signal looks strong. Which contracts are already financed?"
        history = "The demand signal looks strong. I would still check the customer mix.\n"
        result = MODULE.inspect(draft, "reply", 280, history)
        codes = {issue["code"] for issue in result["failures"]}
        self.assertIn("repeated_opener", codes)


if __name__ == "__main__":
    unittest.main()
