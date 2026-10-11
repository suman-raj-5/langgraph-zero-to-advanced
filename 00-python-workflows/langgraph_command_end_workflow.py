
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Command


class ReviewState(TypedDict):
    status: str
    message: str


def review_node(
    state: ReviewState,
) -> Command[Literal["finish", "__end__"]]:
    if state["status"] == "approved":
        return Command(
            update={"message": "Review approved"},
            goto="finish",
        )

    return Command(
        update={"message": "Review rejected"},
        goto=END,
    )


def finish_node(state: ReviewState) -> dict:
    return {"status": "completed"}


def build_graph():
    graph = StateGraph(ReviewState)

    graph.add_node("review", review_node)
    graph.add_node("finish", finish_node)

    graph.add_edge(START, "review")
    graph.add_edge("finish", END)

    return graph.compile()


def main() -> None:
    graph = build_graph()

    result = graph.invoke(
        {
            "status": "approved",
            "message": "",
        }
    )

    print("Final state:")
    print(result)


if __name__ == "__main__":
    main()
