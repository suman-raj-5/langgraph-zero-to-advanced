
import sys
import unittest
from pathlib import Path

WORKFLOW_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKFLOW_DIR))

from composed_workflow import (
    create_summary,
    receive_pull_request,
    validate_pull_request,
)


class TestComposedWorkflow(unittest.TestCase):
    def test_validation_adds_status_without_mutating_input(self):
        pr = receive_pull_request()

        validated_pr = validate_pull_request(pr)

        self.assertEqual(validated_pr["status"], "validated")
        self.assertNotIn("status", pr)
        self.assertEqual(
            validated_pr["pr_number"],
            pr["pr_number"],
        )

    def test_validation_rejects_missing_title(self):
        invalid_pr = {
            "pr_number": 47,
            "title": "",
            "files_changed": ["src/auth.py"],
        }

        with self.assertRaisesRegex(
            ValueError,
            "Pull request title is required",
        ):
            validate_pull_request(invalid_pr)
    
    def test_validation_rejects_empty_files_changed(self):
        invalid_pr = {
            "pr_number": 47,
            "title": "Improve login validation",
            "files_changed": [],
        }

        with self.assertRaisesRegex(
            ValueError,
            "At least one changed file is required",
        ):
            validate_pull_request(invalid_pr)

    def test_summary_counts_changed_files(self):
        pr = receive_pull_request()
        validated_pr = validate_pull_request(pr)

        summary = create_summary(validated_pr)

        self.assertEqual(summary["pr_number"], 47)
        self.assertEqual(summary["status"], "validated")
        self.assertEqual(summary["files_changed_count"], 2)


if __name__ == "__main__":
    unittest.main()
