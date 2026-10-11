
import sys
import unittest
from pathlib import Path

WORKFLOW_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKFLOW_DIR))

from langgraph_fan_in_workflow import build_graph


class TestLangGraphFanInWorkflow(unittest.TestCase):
    def test_fan_in_combines_both_reviews(self):
        graph = build_graph()

        result = graph.invoke(
            {
                "findings": [],
                "completed_reviews": [],
                "summary": "",
            }
        )

        self.assertEqual(
            set(result["completed_reviews"]),
            {"security", "tests"},
        )
        self.assertEqual(len(result["completed_reviews"]), 2)

        self.assertEqual(
            set(result["findings"]),
            {
                "SQL injection risk",
                "Hardcoded secret",
                "Missing test coverage",
            },
        )
        self.assertEqual(len(result["findings"]), 3)

    def test_summary_is_generated_after_both_reviews(self):
        graph = build_graph()

        result = graph.invoke(
            {
                "findings": [],
                "completed_reviews": [],
                "summary": "",
            }
        )

        self.assertEqual(
            result["summary"],
            "Completed 2 reviews; found 3 unique findings.",
        )


if __name__ == "__main__":
    unittest.main()
