
import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph


class ReviewState(TypedDict):
    findings: Annotated[list[str], operator.add]


def security_review(state: ReviewState) -> dict:
    return {
        "findings": ["SQL injection risk"],
    }


def test_review(state: ReviewState) -> dict:
    return {
        "findings": ["Missing test coverage"],
    }


def build_graph():
    graph = StateGraph(ReviewState)

    graph.add_node("security_review", security_review)
    graph.add_node("test_review", test_review)

    graph.add_edge(START, "security_review")
    graph.add_edge("security_review", "test_review")
    graph.add_edge("test_review", END)

    return graph.compile()


def main() -> None:
    graph = build_graph()

    result = graph.invoke({"findings": []})

    print("Final findings:", result["findings"])


if __name__ == "__main__":
    main()
