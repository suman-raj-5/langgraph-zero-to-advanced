
import sys
import unittest
from pathlib import Path


WORKFLOW_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKFLOW_DIR))

from custom_reducer_workflow import merge_unique_findings
from custom_reducer_workflow import build_graph


class TestCustomReducerWorkflow(unittest.TestCase):
    def test_merge_removes_duplicates(self):
        result = merge_unique_findings(
            ["SQL injection", "Missing tests"],
            ["Missing tests", "Hardcoded secret"],
        )

        self.assertEqual(
            result,
            ["SQL injection", "Missing tests", "Hardcoded secret"],
        )

    def test_merge_preserves_first_seen_order(self):
        result = merge_unique_findings(
            ["A", "B"],
            ["C", "A"],
        )

        self.assertEqual(result, ["A", "B", "C"])

    def test_merge_with_empty_incoming(self):
        result = merge_unique_findings(["A"], [])

        self.assertEqual(result, ["A"])

    def test_merge_with_empty_existing(self):
        result = merge_unique_findings([], ["B"])

        self.assertEqual(result, ["B"])

    def test_merge_with_all_duplicates(self):
        result = merge_unique_findings(["A", "B"], ["A", "B"])

        self.assertEqual(result, ["A", "B"])

    def test_merge_does_not_mutate_inputs(self):
        existing = ["A", "B"]
        incoming = ["B", "C"]

        merge_unique_findings(existing, incoming)

        self.assertEqual(existing, ["A", "B"])
        self.assertEqual(incoming, ["B", "C"])
    
    def test_graph_merges_findings_without_duplicates(self):
        graph = build_graph()

        result = graph.invoke({"findings": []})

        self.assertEqual(
            result["findings"],
            ["SQL injection", "Missing tests", "Hardcoded secret"],
        )

    def test_graph_preserves_initial_findings(self):
        graph = build_graph()

        result = graph.invoke({"findings": ["Existing finding"]})

        self.assertEqual(
            result["findings"],
            [
                "Existing finding",
                "SQL injection",
                "Missing tests",
                "Hardcoded secret",
            ],
        )


if __name__ == "__main__":
    unittest.main()
