
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class ReviewState(TypedDict):
    review_count: int
    max_reviews: int
    findings: list[str]
    status: str


def review_findings(state: ReviewState) -> dict:
    review_count = state["review_count"] + 1
    print(f"Review attempt {review_count}")

    # Simulate a problem that never gets resolved.
    return {
        "review_count": review_count,
        "findings": ["Potential issue remains"],
        "status": "needs_review",
    }


def route_after_review(state: ReviewState) -> str:
    # Stop when the business-level attempt limit is reached.
    if state["review_count"] >= state["max_reviews"]:
        return "stop"

    if state["status"] == "approved":
        return "finish"

    return "review_again"


def finish_review(state: ReviewState) -> dict:
    print("Review approved.")
    return {"status": "approved"}


def stop_review(state: ReviewState) -> dict:
    print("Maximum review attempts reached.")
    return {"status": "max_reviews_reached"}


def build_graph():
    graph = StateGraph(ReviewState)

    graph.add_node("review", review_findings)
    graph.add_node("finish", finish_review)
    graph.add_node("stop", stop_review)

    graph.add_edge(START, "review")

    graph.add_conditional_edges(
        "review",
        route_after_review,
        {
            "review_again": "review",
            "finish": "finish",
            "stop": "stop",
        },
    )

    graph.add_edge("finish", END)
    graph.add_edge("stop", END)

    return graph.compile()


def main() -> None:
    graph = build_graph()

    result = graph.invoke(
        {
            "review_count": 0,
            "max_reviews": 5,
            "findings": ["Initial issue"],
            "status": "needs_review",
        }
    )

    print("\nFinal state:")
    print(result)


if __name__ == "__main__":
    main()
