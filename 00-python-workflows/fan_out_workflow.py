
def receive_pull_request() -> dict:
    """Create the initial pull request state."""
    return {
        "pr_number": 47,
        "title": "Improve login validation",
        "files_changed": [
            "src/auth.py",
            "tests/test_auth.py",
        ],
    }


def security_review(pr: dict) -> dict:
    """Simulate an independent security review."""
    print("Running security review...")

    return {
        "review_type": "security",
        "findings": [
            "Check password validation for edge cases",
        ],
    }


def test_review(pr: dict) -> dict:
    """Simulate an independent test review."""
    print("Running test review...")

    return {
        "review_type": "tests",
        "findings": [
            "Add a test for an empty password",
        ],
    }


def combine_reviews(
    pr: dict,
    security_result: dict,
    test_result: dict,
) -> dict:
    """Combine independent review results into one report."""
    all_findings = (
        security_result["findings"] + test_result["findings"]
    )

    return {
        **pr,
        "review_results": {
            "security": security_result,
            "tests": test_result,
        },
        "all_findings": all_findings,
        "total_findings": len(all_findings),
    }


def main() -> None:
    pr = receive_pull_request()

    print("Starting pull request review")
    security_result = security_review(pr)
    test_result = test_review(pr)
    final_report = combine_reviews(
        pr,
        security_result,
        test_result,
    )

    print("\nSecurity result:")
    print(security_result)

    print("\nTest result:")
    print(test_result)

    print("\nCombined review report:")
    print(final_report)


if __name__ == "__main__":
    main()
