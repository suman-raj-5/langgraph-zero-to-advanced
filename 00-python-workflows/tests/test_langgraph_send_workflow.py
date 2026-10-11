
import sys
import unittest
from pathlib import Path

WORKFLOW_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKFLOW_DIR))

from langgraph_send_workflow import build_graph


class TestLangGraphSendWorkflow(unittest.TestCase):
    def setUp(self):
        self.graph = build_graph()

    def test_all_files_are_reviewed(self):
        result = self.graph.invoke(
            {
                "files": ["auth.py", "database.py", "api.py"],
                "findings": [],
            }
        )

        self.assertEqual(len(result["findings"]), 3)
        self.assertEqual(
            set(result["findings"]),
            {
                "Reviewed auth.py",
                "Reviewed database.py",
                "Reviewed api.py",
            },
        )

    def test_findings_are_collected_for_each_file(self):
        result = self.graph.invoke(
            {
                "files": ["auth.py", "api.py"],
                "findings": [],
            }
        )

        self.assertEqual(
            set(result["findings"]),
            {"Reviewed auth.py", "Reviewed api.py"},
        )

    def test_empty_file_list_produces_no_findings(self):
        result = self.graph.invoke(
            {
                "files": [],
                "findings": [],
            }
        )

        self.assertEqual(result["findings"], [])


if __name__ == "__main__":
    unittest.main()
