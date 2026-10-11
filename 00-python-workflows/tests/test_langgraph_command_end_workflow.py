
import sys
import unittest
from pathlib import Path

WORKFLOW_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKFLOW_DIR))

from langgraph_command_end_workflow import build_graph


class TestLangGraphCommandEndWorkflow(unittest.TestCase):
    def setUp(self):
        self.graph = build_graph()

    def test_rejected_review_ends_without_running_finish(self):
        result = self.graph.invoke(
            {
                "status": "rejected",
                "message": "",
            }
        )

        self.assertEqual(result["status"], "rejected")
        self.assertEqual(result["message"], "Review rejected")

    def test_approved_review_runs_finish_before_ending(self):
        result = self.graph.invoke(
            {
                "status": "approved",
                "message": "",
            }
        )

        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["message"], "Review approved")


if __name__ == "__main__":
    unittest.main()
