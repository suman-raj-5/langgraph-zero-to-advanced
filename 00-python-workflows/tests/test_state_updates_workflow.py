
import sys
import unittest
from pathlib import Path

WORKFLOW_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKFLOW_DIR))

from state_updates_workflow import (
    complete_review,
    receive_pull_request,
)


class TestStateUpdatesWorkflow(unittest.TestCase):
    def test_complete_review_updates_status(self):
        state = receive_pull_request()

        updated_state = complete_review(state)

        self.assertEqual(updated_state["status"], "completed")

    def test_complete_review_preserves_existing_fields(self):
        state = receive_pull_request()

        updated_state = complete_review(state)

        self.assertEqual(updated_state["pr_number"], 47)
        self.assertEqual(
            updated_state["title"],
            "Improve login validation",
        )
        self.assertEqual(updated_state["reviewer"], "Alex")

    def test_complete_review_does_not_mutate_original_state(self):
        state = receive_pull_request()

        complete_review(state)

        self.assertEqual(state["status"], "pending")
        self.assertEqual(state["pr_number"], 47)


if __name__ == "__main__":
    unittest.main()
