
from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Command


class ReviewState(TypedDict):
    status: str
    message: str


def review_node(state: ReviewState) -> Command:
    if state["status"] == "approved":
        return Command(
            update={"message": "Review approved"},
            goto="finish",
        )

    return Command(
        update={"message": "More review needed"},
        goto="review_again",
    )


def finish_node(state: ReviewState) -> dict:
    return {"status": "completed"}


def review_again_node(state: ReviewState) -> dict:
    return {"status": "needs_review"}


def build_graph():
    graph = StateGraph(ReviewState)

    graph.add_node("review", review_node)
    graph.add_node("finish", finish_node)
    graph.add_node("review_again", review_again_node)

    graph.add_edge(START, "review")
    graph.add_edge("finish", END)
    graph.add_edge("review_again", END)

    return graph.compile()


def main() -> None:
    graph = build_graph()

    result = graph.invoke(
        {
            "status": "needs_review",
            "message": "",
        }
    )

    print("Final state:")
    print(result)


if __name__ == "__main__":
    main()
