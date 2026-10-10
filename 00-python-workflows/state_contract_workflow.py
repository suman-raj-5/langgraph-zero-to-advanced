
from typing import NotRequired, TypedDict


class ReviewState(TypedDict):
    """Define the expected structure of a pull request review state."""

    pr_number: int
    title: str
    files_changed: int
    status: str
    inspection_result: NotRequired[str]
    summary: NotRequired[str]


def receive_pull_request() -> ReviewState:
    """Create a valid initial workflow state."""
    return {
        "pr_number": 47,
        "title": "Improve login validation",
        "files_changed": 2,
        "status": "pending",
    }


def validate_state(state: ReviewState) -> None:
    """Validate the required fields and values in the workflow state."""

    required_keys = {
        "pr_number",
        "title",
        "files_changed",
        "status",
    }

    missing_keys = required_keys - state.keys()

    if missing_keys:
        raise ValueError(f"Missing required keys: {sorted(missing_keys)}")

    if (
        not isinstance(state["pr_number"], int)
        or isinstance(state["pr_number"], bool)
    ):
        raise ValueError("pr_number must be an integer")

    if not isinstance(state["title"], str) or not state["title"].strip():
        raise ValueError("title must be a non-empty string")

    if (
        not isinstance(state["files_changed"], int)
        or isinstance(state["files_changed"], bool)
    ):
        raise ValueError("files_changed must be an integer")

    if state["files_changed"] < 0:
        raise ValueError("files_changed cannot be negative")

    if state["status"] not in {"pending", "completed", "failed"}:
        raise ValueError("status must be pending, completed, or failed")



def main() -> None:
    state = receive_pull_request()
    validate_state(state)

    print("Initial workflow state:")
    print(state)

    print("\nTesting invalid title:")
    invalid_title_state = {
        "pr_number": 47,
        "title": "",
        "files_changed": 2,
        "status": "pending",
    }

    try:
        validate_state(invalid_title_state)
    except ValueError as error:
        print(f"Validation failed as expected: {error}")

    print("\nTesting invalid pull request number:")
    invalid_number_state = {
        "pr_number": True,
        "title": "Improve login validation",
        "files_changed": 2,
        "status": "pending",
    }

    try:
        validate_state(invalid_number_state)
    except ValueError as error:
        print(f"Validation failed as expected: {error}")

    print("\nAvailable state fields:")
    print(ReviewState.__annotations__)


if __name__ == "__main__":
    main()
