
"""
Lesson 01: Sequential workflow using plain Python.

We execute three steps in a fixed order:
1. Receive a pull request.
2. Inspect its changes.
3. Generate a review summary.
"""


def receive_pull_request() -> dict:
    """Step 1: Create the initial workflow data."""
    print("Step 1: Receiving pull request")

    return {
        "pr_number": 42,
        "title": "Fix authentication validation",
        "files_changed": 3,
    }


def inspect_changes(pr: dict) -> dict:
    """Step 2: Inspect the pull request."""
    print("Step 2: Inspecting changes")

    return {
        **pr,
        "review_status": "changes inspected",
    }


def generate_summary(review: dict) -> dict:
    """Step 3: Generate the final review summary."""
    print("Step 3: Generating summary")

    return {
        **review,
        "summary": (
            f"PR #{review['pr_number']}: "
            f"{review['title']} — "
            f"{review['files_changed']} files changed."
        ),
    }


def main() -> None:
    """Orchestrate the workflow in a fixed sequence."""
    pr = receive_pull_request()
    review = inspect_changes(pr)
    result = generate_summary(review)

    print("\nFinal result:")
    print(result)


if __name__ == "__main__":
    main()
