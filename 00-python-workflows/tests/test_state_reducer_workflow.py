
import sys
import unittest
from pathlib import Path

WORKFLOW_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKFLOW_DIR))

from state_reducer_workflow import merge_findings


class TestStateReducerWorkflow(unittest.TestCase):
    def test_merge_combines_both_lists(self):
        result = merge_findings(
            ["SQL injection risk"],
            ["Missing test coverage"],
        )

        self.assertEqual(
            result,
            ["SQL injection risk", "Missing test coverage"],
        )

    def test_merge_with_empty_incoming_list(self):
        result = merge_findings(["Existing finding"], [])

        self.assertEqual(result, ["Existing finding"])

    def test_merge_with_empty_existing_list(self):
        result = merge_findings([], ["New finding"])

        self.assertEqual(result, ["New finding"])

    def test_merge_preserves_order(self):
        result = merge_findings(
            ["Security issue", "Authentication issue"],
            ["Missing test"],
        )

        self.assertEqual(
            result,
            ["Security issue", "Authentication issue", "Missing test"],
        )

    def test_merge_does_not_mutate_inputs(self):
        existing = ["Existing finding"]
        incoming = ["New finding"]

        result = merge_findings(existing, incoming)

        self.assertEqual(existing, ["Existing finding"])
        self.assertEqual(incoming, ["New finding"])
        self.assertEqual(result, ["Existing finding", "New finding"])


if __name__ == "__main__":
    unittest.main()
