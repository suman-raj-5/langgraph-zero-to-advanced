# Lesson 19 — LangGraph Loops and Recursion Limits

## Objective

Learn how to build cyclic LangGraph workflows, terminate them with application-level conditions, and use LangGraph's recursion limit as a runtime safeguard.

## 1. Controlled review loop

The review workflow repeats until the review is approved or the maximum number of attempts is reached.

```text
START
  |
  v
Review findings
  |
  v
Check stopping condition
  |             \
  | retry        \ maximum reached
  v               v
Review again      Stop
  |
  v
Finish when approved
```

## 2. Application-level stopping condition

The workflow stores a maximum number of review attempts in its state:

```python
class ReviewState(TypedDict):
    review_count: int
    max_reviews: int
    findings: list[str]
    status: str
```

The routing function checks the attempt limit:

```python
if state["review_count"] >= state["max_reviews"]:
    return "stop"
```

This is a business-level rule. It determines when the review process should stop according to the application's requirements.

In the current example, the issue remains unresolved, so the workflow stops after five attempts with the status `max_reviews_reached`.

## 3. LangGraph recursion limit

The second example deliberately creates an unbounded cycle:

```python
graph.add_edge(START, "increment")
graph.add_edge("increment", "increment")
```

There is no route to `END`, so the graph continues until LangGraph's runtime limit is reached.

The invocation config sets a small limit for the demonstration:

```python
graph.invoke(
    {"count": 0},
    config={"recursion_limit": 10},
)
```

LangGraph raises `GraphRecursionError` when the graph cannot reach a stopping condition within that limit.

The recursion limit is a runtime safeguard; it is not a replacement for a proper application-level termination condition.

## 4. Run the bounded workflow

```bash
uv run python 00-python-workflows/langgraph_loop_workflow.py
```

Expected final status:

```text
max_reviews_reached
```

## 5. Run the unbounded-loop demonstration

```bash
uv run python 00-python-workflows/langgraph_recursion_limit_demo.py
```

The example should stop with `GraphRecursionError`, caught and printed by the demonstration.

## 6. Run the lesson tests

```bash
uv run python -m unittest 00-python-workflows/tests/test_langgraph_loop_workflow.py -v
```

Run the complete suite:

```bash
uv run python -m unittest discover -s 00-python-workflows/tests -v
```

The full suite passed with 43 tests when this lesson was verified.

## 7. Exercises

1. Why is a business-level attempt limit better than relying only on the recursion limit?
2. What happens if the loop's routing function never returns a terminal route?
3. Why does `GraphRecursionError` differ from a normal `max_reviews_reached` result?
4. How would you stop a review loop when findings become empty?
5. How would you test that a workflow terminates exactly at the configured maximum?

## Key takeaway

A well-designed cyclic workflow needs explicit termination logic. Application-level conditions enforce business rules, while LangGraph's recursion limit protects against excessive graph execution when the workflow fails to terminate as expected.