
import sys
import unittest
from pathlib import Path

WORKFLOW_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKFLOW_DIR))

from state_contract_workflow import (
    receive_pull_request,
    validate_state,
)


class TestStateContractWorkflow(unittest.TestCase):
    def test_initial_state_is_valid(self):
        state = receive_pull_request()

        validate_state(state)

    def test_negative_files_changed_is_rejected(self):
        state = receive_pull_request()
        state["files_changed"] = -1

        with self.assertRaisesRegex(
            ValueError,
            "files_changed cannot be negative",
        ):
            validate_state(state)

    def test_boolean_files_changed_is_rejected(self):
        state = receive_pull_request()
        state["files_changed"] = True

        with self.assertRaisesRegex(
            ValueError,
            "files_changed must be an integer",
        ):
            validate_state(state)

    def test_invalid_status_is_rejected(self):
        state = receive_pull_request()
        state["status"] = "unknown"

        with self.assertRaisesRegex(
            ValueError,
            "status must be pending, completed, or failed",
        ):
            validate_state(state)


if __name__ == "__main__":
    unittest.main()
