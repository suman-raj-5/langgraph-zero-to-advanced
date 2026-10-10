
def receive_pull_request() -> dict:
    """Return the initial pull request state."""
    return {
        "pr_number": 47,
        "title": "Improve login validation",
        "files_changed": [
            "src/auth.py",
            "tests/test_auth.py",
        ],
    }


def validate_pull_request(pr: dict) -> dict:
    """Validate required pull request fields."""
    if not pr.get("pr_number"):
        raise ValueError("Pull request number is required")

    if not pr.get("title"):
        raise ValueError("Pull request title is required")

    if not pr.get("files_changed"):
        raise ValueError("At least one changed file is required")

    return {
        **pr,
        "status": "validated",
    }


def create_summary(pr: dict) -> dict:
    """Create a summary from a validated pull request."""
    return {
        "pr_number": pr["pr_number"],
        "title": pr["title"],
        "status": pr["status"],
        "files_changed_count": len(pr["files_changed"]),
    }


def demonstrate_validation_failure() -> None:
    """Demonstrate how validation handles an invalid pull request."""
    invalid_pr = {
        "pr_number": 47,
        "title": "",
        "files_changed": ["src/auth.py"],
    }

    try:
        validate_pull_request(invalid_pr)
    except ValueError as error:
        print("\nValidation failed as expected:")
        print(error)


def main() -> None:
    pr = receive_pull_request()
    validated_pr = validate_pull_request(pr)

    print("\nOriginal pull request:")
    print(pr)

    summary = create_summary(validated_pr)

    print("Validated pull request:")
    print(validated_pr)

    print("\nPull request summary:")
    print(summary)
    demonstrate_validation_failure()

if __name__ == "__main__":
    main()
