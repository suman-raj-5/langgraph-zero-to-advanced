import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send


class ReviewState(TypedDict):
    tasks: list[dict[str, str]]
    review_results: Annotated[list[str], operator.add]
    summary: str


class ReviewTask(TypedDict):
    file: str
    content: str


def dispatch_reviews(state: ReviewState) -> list[Send] | str:
    if not state["tasks"]:
        return "summarize_reviews"

    return [
        Send("review_file", task)
        for task in state["tasks"]
    ]


def review_file(task: ReviewTask) -> dict:
    file = task["file"]
    content = task["content"]

    result = (
        f"Reviewed {file}: "
        f"{len(content)} characters examined"
    )

    print(result)

    return {"review_results": [result]}


def summarize_reviews(state: ReviewState) -> dict:
    results = state["review_results"]

    summary = (
        f"Review complete: {len(results)} files reviewed."
    )

    print(summary)

    return {"summary": summary}


def build_graph():
    graph = StateGraph(ReviewState)

    graph.add_node("review_file", review_file)
    graph.add_node("summarize_reviews", summarize_reviews)

    graph.add_conditional_edges(START, dispatch_reviews)

    graph.add_edge("review_file", "summarize_reviews")
    graph.add_edge("summarize_reviews", END)

    return graph.compile()


def main() -> None:
    initial_state: ReviewState = {
        "tasks": [
            {
                "file": "auth.py",
                "content": "def login(): pass",
            },
            {
                "file": "database.py",
                "content": "SELECT * FROM users",
            },
            {
                "file": "api.py",
                "content": "def get_users(): pass",
            },
        ],
        "review_results": [],
        "summary": "",
    }

    result = build_graph().invoke(initial_state)

    print("\nFinal review results:")
    for review in result["review_results"]:
        print(f"- {review}")

    print(f"\nSummary: {result['summary']}")


if __name__ == "__main__":
    main()