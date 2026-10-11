
from typing import Annotated, Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from custom_reducer_workflow import merge_unique_findings


class ReviewState(TypedDict):
    findings: Annotated[list[str], merge_unique_findings]
    completed_reviews: Annotated[list[str], merge_unique_findings]
    summary: str
    next_step: str


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


def route_after_reviews(
    state: ReviewState,
) -> Literal["remediation", "final_report"]:
    has_security_finding = any(
        "security" in finding.lower()
        or "sql injection" in finding.lower()
        or "hardcoded secret" in finding.lower()
        for finding in state["findings"]
    )

    if has_security_finding:
        return "remediation"

    return "final_report"


def remediation(state: ReviewState) -> dict:
    print("Security findings detected; remediation is required.")

    return {"next_step": "remediation_required"}


def final_report(state: ReviewState) -> dict:
    print("No security findings detected; proceeding to final report.")

    return {"next_step": "final_report"}


def build_graph():
    graph = StateGraph(ReviewState)

    graph.add_node("security_review", security_review)
    graph.add_node("test_review", test_review)
    graph.add_node("combine_reviews", combine_reviews)
    graph.add_node("remediation", remediation)
    graph.add_node("final_report", final_report)

    graph.add_edge(START, "security_review")
    graph.add_edge(START, "test_review")

    # Wait for both parallel branches before combining results.
    graph.add_edge(
        ["security_review", "test_review"],
        "combine_reviews",
    )

    # Route only after the combined state is available.
    graph.add_conditional_edges(
        "combine_reviews",
        route_after_reviews,
        {
            "remediation": "remediation",
            "final_report": "final_report",
        },
    )

    graph.add_edge("remediation", END)
    graph.add_edge("final_report", END)

    return graph.compile()


def main() -> None:
    graph = build_graph()

    result = graph.invoke(
        {
            "findings": [],
            "completed_reviews": [],
            "summary": "",
            "next_step": "",
        }
    )

    print("\nFinal findings:")
    for finding in result["findings"]:
        print(f"- {finding}")

    print(f"\nSummary: {result['summary']}")
    print(f"Next step: {result['next_step']}")


if __name__ == "__main__":
    main()
