
import sys
import unittest
from pathlib import Path

WORKFLOW_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKFLOW_DIR))

from routing_comparison_workflow import (
    build_command_graph,
    build_conditional_graph,
)


class TestRoutingComparisonWorkflow(unittest.TestCase):
    def setUp(self):
        self.graphs = {
            "conditional": build_conditional_graph(),
            "command": build_command_graph(),
        }

    def test_approved_results_match(self):
        initial_state = {
            "status": "approved",
            "message": "",
        }

        results = {
            name: graph.invoke(initial_state)
            for name, graph in self.graphs.items()
        }

        self.assertEqual(results["conditional"], results["command"])
        self.assertEqual(results["command"]["status"], "completed")
        self.assertEqual(
            results["command"]["message"],
            "Review approved",
        )

    def test_unapproved_results_match(self):
        initial_state = {
            "status": "needs_review",
            "message": "",
        }

        results = {
            name: graph.invoke(initial_state)
            for name, graph in self.graphs.items()
        }

        self.assertEqual(results["conditional"], results["command"])
        self.assertEqual(results["command"]["status"], "needs_review")
        self.assertEqual(
            results["command"]["message"],
            "More review needed",
        )


if __name__ == "__main__":
    unittest.main()
