
def call_unreliable_service(attempt: int) -> str:
    """Simulate a service that fails twice, then succeeds."""
    print(f"Calling service on attempt {attempt}...")

    if attempt < 3:
        raise ConnectionError("Temporary service failure")

    return "Review data received successfully"


def run_with_retries(max_attempts: int = 5) -> dict:
    """Retry a failed operation until it succeeds or attempts run out."""
    state = {
        "attempt": 0,
        "max_attempts": max_attempts,
        "status": "pending",
        "result": None,
        "error": None,
    }

    while state["attempt"] < state["max_attempts"]:
        state["attempt"] += 1

        try:
            result = call_unreliable_service(state["attempt"])
            state["result"] = result
            state["status"] = "completed"
            state["error"] = None
            break

        except ConnectionError as error:
            state["error"] = str(error)
            print(f"Attempt {state['attempt']} failed: {error}")

    if state["status"] != "completed":
        state["status"] = "failed"

    return state


def main() -> None:
    final_state = run_with_retries()
    print("\nFinal state:")
    print(final_state)


if __name__ == "__main__":
    main()
