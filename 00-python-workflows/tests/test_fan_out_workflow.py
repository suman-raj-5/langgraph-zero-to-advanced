
import unittest

from fan_out_workflow import (
    combine_reviews,
    receive_pull_request,
    security_review,
    test_review,
)


class TestFanOutWorkflow(unittest.TestCase):
    def test_receive_pull_request_returns_expected_state(self):
        pr = receive_pull_request()

        self.assertEqual(pr["pr_number"], 47)
        self.assertEqual(pr["title"], "Improve login validation")
        self.assertEqual(
            pr["files_changed"],
            ["src/auth.py", "tests/test_auth.py"],
        )

    def test_combine_reviews_merges_findings(self):
        pr = receive_pull_request()

        security_result = {
            "review_type": "security",
            "findings": ["Check input validation"],
        }
        test_result = {
            "review_type": "tests",
            "findings": ["Add an invalid-input test"],
        }

        report = combine_reviews(pr, security_result, test_result)

        self.assertEqual(report["pr_number"], 47)
        self.assertEqual(
            report["all_findings"],
            [
                "Check input validation",
                "Add an invalid-input test",
            ],
        )
        self.assertEqual(report["total_findings"], 2)
        self.assertIn("review_results", report)

    def test_combine_reviews_handles_empty_findings(self):
        pr = receive_pull_request()

        security_result = {
            "review_type": "security",
            "findings": [],
        }
        test_result = {
            "review_type": "tests",
            "findings": ["Add an invalid-input test"],
        }

        report = combine_reviews(pr, security_result, test_result)

        self.assertEqual(
            report["all_findings"],
            ["Add an invalid-input test"],
        )
        self.assertEqual(report["total_findings"], 1)
        self.assertEqual(
            report["total_findings"],
            len(report["all_findings"]),
        )

    def test_security_review_returns_security_findings(self):
        pr = receive_pull_request()

        result = security_review(pr)

        self.assertEqual(result["review_type"], "security")
        self.assertIn(
            "Check password validation for edge cases",
            result["findings"],
        )

    def test_test_review_returns_test_findings(self):
        pr = receive_pull_request()

        result = test_review(pr)

        self.assertEqual(result["review_type"], "tests")
        self.assertIn(
            "Add a test for an empty password",
            result["findings"],
        )


if __name__ == "__main__":
    unittest.main()
