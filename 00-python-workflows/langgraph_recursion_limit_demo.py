
from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.errors import GraphRecursionError


class LoopState(TypedDict):
    count: int


def increment(state: LoopState) -> dict:
    count = state["count"] + 1
    print(f"Iteration {count}")
    return {"count": count}


def build_graph():
    graph = StateGraph(LoopState)

    graph.add_node("increment", increment)

    graph.add_edge(START, "increment")
    graph.add_edge("increment", "increment")

    return graph.compile()


def main() -> None:
    graph = build_graph()

    try:
        graph.invoke(
            {"count": 0},
            config={"recursion_limit": 10},
        )
    except GraphRecursionError as error:
        print("\nGraph stopped by LangGraph's recursion limit.")
        print(type(error).__name__)
        print(str(error))


if __name__ == "__main__":
    main()
