
from typing import NotRequired, TypedDict


class ReviewState(TypedDict):
    pr_number: int
    title: str
    files_changed: int
    inspection_result: NotRequired[str]
    summary: NotRequired[str]
    status: str


def receive_pull_request() -> ReviewState:
    """Create the initial workflow state."""
    return {
        "pr_number": 42,
        "title": "Fix authentication validation",
        "files_changed": 3,
        "status": "pending",
    }


def inspect_changes(state: ReviewState) -> ReviewState:
    """Add inspection results without losing existing fields."""
    return {
        **state,
        "inspection_result": "Changes inspected successfully",
    }

def generate_summary(state: ReviewState) -> ReviewState:
    """Add a summary using information already in the state."""
    return {
        **state,
        "summary": (
            f"PR #{state['pr_number']}: {state['title']}. "
            f"Files changed: {state['files_changed']}. "
            f"{state['inspection_result']}."
        ),
    }


def complete_review(state: ReviewState) -> ReviewState:
    """Mark the review as completed without losing existing state."""
    return {
        **state,
        "status": "completed",
    }


def main() -> None:
    state = receive_pull_request()
    print("Initial state:")
    print(state)

    state = inspect_changes(state)
    print("\nAfter inspection:")
    print(state)

    state = generate_summary(state)
    print("\nFinal state:")
    print(state)

    state = complete_review(state)
    print("\nAfter completing review:")
    print(state)

if __name__ == "__main__":
    main()
