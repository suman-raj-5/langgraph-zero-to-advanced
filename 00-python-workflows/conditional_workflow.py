
"""
Lesson 02: Conditional workflow using plain Python.

A routing function selects the next step based on workflow data.
"""


def receive_pull_request() -> dict:
    """Create sample pull-request data."""
    print("Receiving pull request")
    
    return {
        "pr_number": 44,
        "title": "Update product catalog",
        "files_changed": [
            "src/catalog.py",
            "tests/test_catalog.py",
        ],
    }


def route_review(pr: dict) -> str:
    """Choose a review path based on the changed files."""
    print("Deciding review path")

    if any("auth" in filename.lower() for filename in pr["files_changed"]):
        return "security_review"

    return "standard_review"


def security_review(pr: dict) -> dict:
    """Handle pull requests that touch authentication code."""
    print("Running security review")

    return {
        **pr,
        "review_type": "security",
        "review_status": "security review completed",
    }


def standard_review(pr: dict) -> dict:
    """Handle other pull requests."""
    print("Running standard review")

    return {
        **pr,
        "review_type": "standard",
        "review_status": "standard review completed",
    }


def main() -> None:
    pr = receive_pull_request()

    route = route_review(pr)
    print(f"Selected route: {route}")

    if route == "security_review":
        result = security_review(pr)
    else:
        result = standard_review(pr)

    print("\nFinal result:")
    print(result)


if __name__ == "__main__":
    main()
