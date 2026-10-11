
import sys
import unittest
from pathlib import Path

WORKFLOW_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKFLOW_DIR))

from langgraph_conditional_fan_in_workflow import (
    build_graph,
    route_after_reviews,
)


class TestLangGraphConditionalFanInWorkflow(unittest.TestCase):
    def test_security_findings_route_to_remediation(self):
        graph = build_graph()

        result = graph.invoke(
            {
                "findings": [],
                "completed_reviews": [],
                "summary": "",
                "next_step": "",
            }
        )

        self.assertEqual(result["next_step"], "remediation_required")
        self.assertEqual(len(result["completed_reviews"]), 2)
        self.assertEqual(len(result["findings"]), 3)

    def test_findings_without_security_risk_route_to_report(self):
        state = {
            "findings": ["Missing test coverage"],
            "completed_reviews": ["security", "tests"],
            "summary": "Completed 2 reviews; found 1 unique finding.",
            "next_step": "",
        }

        self.assertEqual(route_after_reviews(state), "final_report")

    def test_security_findings_are_detected_case_insensitively(self):
        state = {
            "findings": ["SQL INJECTION risk"],
            "completed_reviews": [],
            "summary": "",
            "next_step": "",
        }

        self.assertEqual(route_after_reviews(state), "remediation")


if __name__ == "__main__":
    unittest.main()
