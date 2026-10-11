
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Command


class ReviewState(TypedDict):
    status: str
    message: str


# Approach 1: Conditional edges


def review_with_conditional_edges(state: ReviewState) -> dict:
    if state["status"] == "approved":
        return {"message": "Review approved"}

    return {"message": "More review needed"}


def route_review(state: ReviewState) -> Literal["finish", "review_again"]:
    if state["status"] == "approved":
        return "finish"

    return "review_again"


# Approach 2: Command


def review_with_command(
    state: ReviewState,
) -> Command[Literal["finish", "review_again"]]:
    if state["status"] == "approved":
        return Command(
            update={"message": "Review approved"},
            goto="finish",
        )

    return Command(
        update={"message": "More review needed"},
        goto="review_again",
    )


# Shared destination nodes


def finish_node(state: ReviewState) -> dict:
    return {"status": "completed"}


def review_again_node(state: ReviewState) -> dict:
    return {"status": "needs_review"}


def build_conditional_graph():
    graph = StateGraph(ReviewState)

    graph.add_node("review", review_with_conditional_edges)
    graph.add_node("finish", finish_node)
    graph.add_node("review_again", review_again_node)

    graph.add_edge(START, "review")

    graph.add_conditional_edges(
        "review",
        route_review,
        {
            "finish": "finish",
            "review_again": "review_again",
        },
    )

    graph.add_edge("finish", END)
    graph.add_edge("review_again", END)

    return graph.compile()


def build_command_graph():
    graph = StateGraph(ReviewState)

    graph.add_node("review", review_with_command)
    graph.add_node("finish", finish_node)
    graph.add_node("review_again", review_again_node)

    graph.add_edge(START, "review")
    graph.add_edge("finish", END)
    graph.add_edge("review_again", END)

    return graph.compile()


def main() -> None:
    initial_state: ReviewState = {
        "status": "needs_review",
        "message": "",
    }

    conditional_result = build_conditional_graph().invoke(initial_state)
    command_result = build_command_graph().invoke(initial_state)

    print("Conditional edges:")
    print(conditional_result)

    print("\nCommand:")
    print(command_result)


if __name__ == "__main__":
    main()
