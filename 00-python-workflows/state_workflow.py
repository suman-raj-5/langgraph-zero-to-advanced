from typing import TypedDict


class ReviewState(TypedDict):
    pr_number: int
    title: str
    files_changed: int
    status: str



def receive_pull_request() -> ReviewState:
    """Create the initial state for a pull request review."""
    return {
        "pr_number": 42,
        "title": "Fix authentication validation",
        "files_changed": 3,
        "status": "pending",
    }


def validate_state(state: ReviewState) -> None:
    """Raise ValueError when the workflow state is invalid."""
    required_keys = {
        "pr_number",
        "title",
        "files_changed",
        "status",
    }

    missing_keys = required_keys - state.keys()

    if missing_keys:
        raise ValueError(f"Missing required keys: {sorted(missing_keys)}")

    if not isinstance(state["pr_number"], int) or isinstance(state["pr_number"], bool):
        raise ValueError("pr_number must be an integer")

    if not isinstance(state["title"], str) or not state["title"].strip():
        raise ValueError("title must be a non-empty string")

    if not isinstance(state["files_changed"], int) or isinstance(state["files_changed"], bool):
        raise ValueError("files_changed must be an integer")

    if state["files_changed"] < 0:
        raise ValueError("files_changed cannot be negative")

    if state["status"] not in {"pending", "completed", "failed"}:
        raise ValueError("status must be pending, completed, or failed")


def main() -> None:
    state = receive_pull_request()
    validate_state(state)

    print("State is valid:")
    print(state)


if __name__ == "__main__":
    main()
