
import sys
import unittest
from pathlib import Path

WORKFLOW_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKFLOW_DIR))

from parallel_reducer_workflow import build_graph


class TestParallelReducerWorkflow(unittest.TestCase):
    def test_parallel_branches_contribute_all_unique_findings(self):
        graph = build_graph()

        result = graph.invoke({"findings": []})

        self.assertEqual(
            set(result["findings"]),
            {
                "SQL injection risk",
                "Hardcoded secret",
                "Missing test coverage",
            },
        )
        self.assertEqual(len(result["findings"]), 3)

    def test_parallel_branches_preserve_initial_findings(self):
        graph = build_graph()

        result = graph.invoke({"findings": ["Existing finding"]})

        self.assertEqual(
            set(result["findings"]),
            {
                "Existing finding",
                "SQL injection risk",
                "Hardcoded secret",
                "Missing test coverage",
            },
        )
        self.assertEqual(len(result["findings"]), 4)


if __name__ == "__main__":
    unittest.main()
