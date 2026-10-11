
import sys
import unittest
from pathlib import Path

WORKFLOW_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKFLOW_DIR))

from langgraph_send_custom_state_workflow import build_graph


class TestLangGraphSendCustomStateWorkflow(unittest.TestCase):
    def setUp(self):
        self.graph = build_graph()

    def test_each_worker_uses_its_custom_task_input(self):
        result = self.graph.invoke(
            {
                "tasks": [
                    {
                        "file": "auth.py",
                        "content": "def login(): pass",
                        "category": "security",
                    },
                    {
                        "file": "database.py",
                        "content": "SELECT * FROM users",
                        "category": "SQL",
                    },
                ],
                "findings": [],
            }
        )

        self.assertEqual(
            set(result["findings"]),
            {
                "security review of auth.py: 17 characters examined",
                "SQL review of database.py: 19 characters examined",
            },
        )

    def test_empty_tasks_produce_no_findings(self):
        result = self.graph.invoke(
            {
                "tasks": [],
                "findings": [],
            }
        )

        self.assertEqual(result["findings"], [])


if __name__ == "__main__":
    unittest.main()
