
import sys
import unittest
from pathlib import Path

WORKFLOW_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKFLOW_DIR))

from langgraph_command_workflow import build_graph


class TestLangGraphCommandWorkflow(unittest.TestCase):
    def setUp(self):
        self.graph = build_graph()

    def test_approved_review_routes_to_finish(self):
        result = self.graph.invoke(
            {
                "status": "approved",
                "message": "",
            }
        )

        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["message"], "Review approved")

    def test_unapproved_review_routes_to_review_again(self):
        result = self.graph.invoke(
            {
                "status": "needs_review",
                "message": "",
            }
        )

        self.assertEqual(result["status"], "needs_review")
        self.assertEqual(result["message"], "More review needed")


if __name__ == "__main__":
    unittest.main()
