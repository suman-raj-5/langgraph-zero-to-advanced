
import sys
import unittest
from pathlib import Path

WORKFLOW_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKFLOW_DIR))

from langgraph.errors import GraphRecursionError
from langgraph_loop_workflow import build_graph
from langgraph_recursion_limit_demo import build_graph as build_unbounded_graph


class TestLangGraphLoopWorkflow(unittest.TestCase):
    def test_loop_stops_at_maximum_review_count(self):
        graph = build_graph()

        result = graph.invoke(
            {
                "review_count": 0,
                "max_reviews": 5,
                "findings": ["Initial issue"],
                "status": "needs_review",
            }
        )

        self.assertEqual(result["review_count"], 5)
        self.assertEqual(result["status"], "max_reviews_reached")
        self.assertEqual(result["findings"], ["Potential issue remains"])

    def test_loop_respects_a_different_maximum(self):
        graph = build_graph()

        result = graph.invoke(
            {
                "review_count": 0,
                "max_reviews": 2,
                "findings": ["Initial issue"],
                "status": "needs_review",
            }
        )

        self.assertEqual(result["review_count"], 2)
        self.assertEqual(result["status"], "max_reviews_reached")

    def test_unbounded_graph_raises_recursion_limit_error(self):
        graph = build_unbounded_graph()

        with self.assertRaises(GraphRecursionError):
            graph.invoke(
                {"count": 0},
                config={"recursion_limit": 5},
            )


if __name__ == "__main__":
    unittest.main()
