
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph

from custom_reducer_workflow import merge_unique_findings


class ReviewState(TypedDict):
    findings: Annotated[list[str], merge_unique_findings]
    completed_reviews: Annotated[list[str], merge_unique_findings]
    summary: str


def security_review(state: ReviewState) -> dict:
    print("Security review running...")

    return {
        "findings": ["SQL injection risk", "Hardcoded secret"],
        "completed_reviews": ["security"],
    }


def test_review(state: ReviewState) -> dict:
    print("Test review running...")

    return {
        "findings": ["Missing test coverage", "Hardcoded secret"],
        "completed_reviews": ["tests"],
    }


def combine_reviews(state: ReviewState) -> dict:
    print("Combining reviews...")

    return {
        "summary": (
            f"Completed {len(state['completed_reviews'])} reviews; "
            f"found {len(state['findings'])} unique findings."
        )
    }


def build_graph():
    graph = StateGraph(ReviewState)

    graph.add_node("security_review", security_review)
    graph.add_node("test_review", test_review)
    graph.add_node("combine_reviews", combine_reviews)

    graph.add_edge(START, "security_review")
    graph.add_edge(START, "test_review")

    # Fan-in: wait for BOTH review branches.
    graph.add_edge(
        ["security_review", "test_review"],
        "combine_reviews",
    )

    graph.add_edge("combine_reviews", END)

    return graph.compile()


def main() -> None:
    graph = build_graph()

    result = graph.invoke(
        {
            "findings": [],
            "completed_reviews": [],
            "summary": "",
        }
    )

    print("\nFinal findings:")
    for finding in result["findings"]:
        print(f"- {finding}")

    print(f"\nSummary: {result['summary']}")


if __name__ == "__main__":
    main()
