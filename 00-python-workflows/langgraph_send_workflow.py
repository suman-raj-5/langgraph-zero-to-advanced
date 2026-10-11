
import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send


class ReviewState(TypedDict):
    files: list[str]
    findings: Annotated[list[str], operator.add]


class FileReviewState(TypedDict):
    file: str


def dispatch_reviews(state: ReviewState) -> list[Send]:
    return [
        Send("review_file", {"file": file})
        for file in state["files"]
    ]


def review_file(state: FileReviewState) -> dict:
    file = state["file"]
    finding = f"Reviewed {file}"
    print(finding)

    return {"findings": [finding]}


def build_graph():
    graph = StateGraph(ReviewState)

    graph.add_node("review_file", review_file)

    graph.add_conditional_edges(
        START,
        dispatch_reviews,
    )

    graph.add_edge("review_file", END)

    return graph.compile()


def main() -> None:
    result = build_graph().invoke(
        {
            "files": ["auth.py", "database.py", "api.py"],
            "findings": [],
        }
    )

    print("\nFinal findings:")
    print(result["findings"])


if __name__ == "__main__":
    main()
