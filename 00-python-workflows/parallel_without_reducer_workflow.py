
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from custom_reducer_workflow import merge_unique_findings

class ReviewState(TypedDict):
    findings: Annotated[list[str], merge_unique_findings]


def security_review(state: ReviewState) -> dict:
    print("Security review running...")

    return {
        "findings": [
            "SQL injection risk",
            "Hardcoded secret",
        ]
    }


def test_review(state: ReviewState) -> dict:
    print("Test review running...")

    return {
        "findings": [
            "Missing test coverage",
            "Hardcoded secret",
        ]
    }


def build_graph():
    graph = StateGraph(ReviewState)

    graph.add_node("security_review", security_review)
    graph.add_node("test_review", test_review)

    graph.add_edge(START, "security_review")
    graph.add_edge(START, "test_review")

    graph.add_edge("security_review", END)
    graph.add_edge("test_review", END)

    return graph.compile()


def main() -> None:
    graph = build_graph()

    result = graph.invoke({"findings": []})

    print("\nFinal findings:")
    print(result["findings"])


if __name__ == "__main__":
    main()
