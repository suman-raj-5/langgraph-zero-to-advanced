import copy
import sys
import unittest
from pathlib import Path

WORKFLOW_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKFLOW_DIR))

from langgraph_map_reduce_workflow import build_graph


class TestLangGraphMapReduceWorkflow(unittest.TestCase):
    def setUp(self):
        self.graph = build_graph()

    def test_all_tasks_are_reviewed_and_summarized(self):
        result = self.graph.invoke(
            {
                "tasks": [
                    {"file": "auth.py", "content": "login code"},
                    {"file": "database.py", "content": "query code"},
                    {"file": "api.py", "content": "endpoint code"},
                ],
                "review_results": [],
                "summary": "",
            }
        )

        self.assertEqual(len(result["review_results"]), 3)
        self.assertEqual(
            {item.split(":")[0] for item in result["review_results"]},
            {
                "Reviewed auth.py",
                "Reviewed database.py",
                "Reviewed api.py",
            },
        )
        self.assertEqual(
            result["summary"],
            "Review complete: 3 files reviewed.",
        )

    def test_empty_tasks_produce_empty_results_and_summary(self):
        result = self.graph.invoke(
            {
                "tasks": [],
                "review_results": [],
                "summary": "",
            }
        )

        self.assertEqual(result["review_results"], [])
        self.assertEqual(
            result["summary"],
            "Review complete: 0 files reviewed.",
        )

    def test_original_input_state_is_not_mutated(self):
        initial_state = {
            "tasks": [
                {"file": "auth.py", "content": "login code"},
                {"file": "api.py", "content": "endpoint code"},
            ],
            "review_results": [],
            "summary": "",
        }
        original_state = copy.deepcopy(initial_state)

        self.graph.invoke(initial_state)

        self.assertEqual(initial_state, original_state)


if __name__ == "__main__":
    unittest.main()