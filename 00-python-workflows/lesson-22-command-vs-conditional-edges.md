
# Lesson 22 — Command vs Conditional Edges

## Objective

Compare two LangGraph routing approaches: conditional edges and `Command`. Understand their behavior, differences, and when to use each.

## 1. Conditional edges

With conditional edges, the node updates state and a separate routing function chooses the next node.

```python
def review_node(state: ReviewState) -> dict:
    if state["status"] == "approved":
        return {"message": "Review approved"}

    return {"message": "More review needed"}


def route_review(state: ReviewState) -> Literal["finish", "review_again"]:
    if state["status"] == "approved":
        return "finish"

    return "review_again"
```

The graph connects the routing function's results to destination nodes with `add_conditional_edges`.

## 2. Command

With `Command`, a node can update state and select the next node in one return value.

```python
def review_node(
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
```

The destination is selected by `goto`.

## 3. Behavioral equivalence

Both implementations use the same destination nodes:

```text
START
  |
  v
Review
  |
  +-- approved --> finish --> END
  |
  +-- otherwise -> review_again --> END
```

The comparison workflow verifies that both approaches produce identical final states for approved and unapproved inputs.

## 4. Key differences

| Conditional edges | Command |
|---|---|
| Routing is defined separately from node logic | Routing is returned by the node |
| Can keep routing decisions centralized | Can keep a decision, state update, and destination together |
| Useful when routing logic should be independently maintained | Useful when a node's decision determines both its update and destination |

Neither approach is universally better. Choose the one that makes the workflow easier to understand and maintain.

## 5. Run the comparison

```bash
uv run python 00-python-workflows/routing_comparison_workflow.py
```

Change the initial state in `main()` to test both `"approved"` and `"needs_review"`.

Both graphs should produce the same result for each input.

## 6. Run the tests

Run this lesson's tests:

```bash
uv run python -m unittest 00-python-workflows/tests/test_routing_comparison_workflow.py -v
```

Run the complete suite:

```bash
uv run python -m unittest discover -s 00-python-workflows/tests -v
```

The complete suite passed with 49 tests during verification.

## 7. Exercises

1. Where does the routing decision live in each approach?
2. Why do both graphs produce equivalent results?
3. When might separating routing logic improve maintainability?
4. When might `Command` make a node easier to understand?
5. Can `Command` replace every use of conditional edges without affecting readability?

## Key takeaway

Conditional edges and `Command` can express equivalent routing behavior. Conditional edges separate routing from node logic; `Command` combines a state update and routing decision. Choose based on clarity, maintainability, and the needs of the workflow.
