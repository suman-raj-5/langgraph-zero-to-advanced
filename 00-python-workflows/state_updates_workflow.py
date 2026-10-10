
from typing import TypedDict


class ReviewState(TypedDict):
    pr_number: int
    title: str
    status: str
    reviewer: str


def receive_pull_request() -> ReviewState:
    """Create the initial workflow state."""
    return {
        "pr_number": 47,
        "title": "Improve login validation",
        "status": "pending",
        "reviewer": "Alex",
    }


def complete_review(state: ReviewState) -> ReviewState:
    """Update the status while preserving all other fields."""
    return {
        **state,
        "status": "completed",
    }


def main() -> None:
    state = receive_pull_request()

    print("Initial state:")
    print(state)

    updated_state = complete_review(state)

    print("\nUpdated state:")
    print(updated_state)

    print("\nOriginal state after update:")
    print(state)


if __name__ == "__main__":
    main()
