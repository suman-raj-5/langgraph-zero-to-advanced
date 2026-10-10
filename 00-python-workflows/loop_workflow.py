
"""
Lesson 03: Looping workflow using plain Python.

Repeat a review step until the quality threshold is met
or the maximum number of attempts is reached.
"""


def receive_pull_request() -> dict:
    """Create the initial workflow state."""
    print("Receiving pull request")

    return {
        "pr_number": 45,
        "attempt": 0,
        "quality_score": 0,
        "target_score": 3,
        "max_attempts": 5,
    }


def review_iteration(state: dict) -> dict:
    """Run one review iteration and return updated state."""
    attempt = state["attempt"] + 1

    # Simulate improvement on each attempt.
    quality_score = min(attempt, state["target_score"])

    print(
        f"Attempt {attempt}: "
        f"quality score = {quality_score}"
    )

    return {
        **state,
        "attempt": attempt,
        "quality_score": quality_score,
    }


def main() -> None:
    state = receive_pull_request()

    while (
        state["quality_score"] < state["target_score"]
        and state["attempt"] < state["max_attempts"]
    ):
        state = review_iteration(state)

    if state["quality_score"] >= state["target_score"]:
        state = {
            **state,
            "status": "completed",
        }
    else:
        state = {
            **state,
            "status": "maximum attempts reached",
        }

    print("\nFinal state:")
    print(state)


if __name__ == "__main__":
    main()
