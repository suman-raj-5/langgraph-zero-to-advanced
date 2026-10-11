
import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send


class ReviewState(TypedDict):
    tasks: list[dict[str, str]]
    findings: Annotated[list[str], operator.add]


class ReviewTask(TypedDict):
    file: str
    content: str
    category: str


def dispatch_reviews(state: ReviewState) -> list[Send]:
    return [
        Send("review_file", task)
        for task in state["tasks"]
    ]


def review_file(task: ReviewTask) -> dict:
    file = task["file"]
    content = task["content"]
    category = task["category"]

    finding = (
        f"{category} review of {file}: "
        f"{len(content)} characters examined"
    )
    print(finding)

    return {"findings": [finding]}


def build_graph():
    graph = StateGraph(ReviewState)

    graph.add_node("review_file", review_file)
    graph.add_conditional_edges(START, dispatch_reviews)
    graph.add_edge("review_file", END)

    return graph.compile()


def main() -> None:
    result = build_graph().invoke(
        {
            "tasks": [
                {
                    "file": "auth.py",
                    "content": "def login(): pass",
                    "category": "security",
                },
                {
                    "file": "database.py",
                    "content": "SELECT * FROM users",
                    "category": "SQL",
                },
            ],
            "findings": [],
        }
    )

    print("\nFinal findings:")
    for finding in result["findings"]:
        print(f"- {finding}")


if __name__ == "__main__":
    main()
