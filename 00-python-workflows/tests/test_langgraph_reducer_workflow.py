
import sys
import unittest
from pathlib import Path

WORKFLOW_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKFLOW_DIR))

from langgraph_reducer_workflow import build_graph


class TestLangGraphReducerWorkflow(unittest.TestCase):
    def test_reducer_combines_findings_from_both_nodes(self):
        graph = build_graph()

        result = graph.invoke({"findings": []})

        self.assertEqual(
            result["findings"],
            ["SQL injection risk", "Missing test coverage"],
        )

    def test_reducer_preserves_initial_findings(self):
        graph = build_graph()

        result = graph.invoke({"findings": ["Existing finding"]})

        self.assertEqual(
            result["findings"],
            [
                "Existing finding",
                "SQL injection risk",
                "Missing test coverage",
            ],
        )


if __name__ == "__main__":
    unittest.main()
