# Lesson 17 — LangGraph Fan-in and Synchronization

## Objective

Understand how parallel branches can run concurrently and how a fan-in edge ensures that a downstream node waits for multiple upstream branches to finish.

## 1. Graph structure

```text
             START
             /   \
            v     v
       Security    Test
        Review    Review
            \      /
             v    v
        Combine Reviews
              |
              v
             END
```

## 2. Fan-out

Both review nodes are connected to `START`:

```python
graph.add_edge(START, "security_review")
graph.add_edge(START, "test_review")
```

This allows LangGraph to schedule both review branches in the same execution step.

## 3. Fan-in synchronization

The key edge is:

```python
graph.add_edge(
    ["security_review", "test_review"],
    "combine_reviews",
)
```

This creates a fan-in synchronization point. The `combine_reviews` node runs after both specified upstream nodes complete.

The summary can therefore use the results contributed by both review branches.

## 4. Reducers and execution control

The workflow uses reducers for shared list fields:

```python
class ReviewState(TypedDict):
    findings: Annotated[list[str], merge_unique_findings]
    completed_reviews: Annotated[list[str], merge_unique_findings]
    summary: str
```

The responsibilities are different:

- **Reducers** determine how updates to a shared state key are merged.
- **Graph edges** determine which nodes run and when.
- **Fan-in edges** synchronize downstream execution with multiple upstream nodes.

A reducer alone does not create a synchronization barrier.

## 5. Expected result

The example produces three unique findings:

- SQL injection risk
- Hardcoded secret
- Missing test coverage

The summary is:

```text
Completed 2 reviews; found 3 unique findings.
```

## 6. Run the workflow

```bash
uv run python 00-python-workflows/langgraph_fan_in_workflow.py
```

## 7. Run the lesson tests

```bash
uv run python -m unittest 00-python-workflows/tests/test_langgraph_fan_in_workflow.py -v
```

Run the full test suite:

```bash
uv run python -m unittest discover -s 00-python-workflows/tests -v
```

The full suite passed with 37 tests when this lesson was verified.

## 8. Exercises

1. What is the difference between fan-out and fan-in?
2. Why should `combine_reviews` wait for both review nodes?
3. What information could be missing if the summary ran after only one branch?
4. Why are reducers still necessary when a fan-in edge already exists?
5. What would change if the graph had three review branches?

## Key takeaway

Fan-in is an execution synchronization mechanism. It ensures that downstream work waits for the required upstream branches, while reducers define how those branches' state updates are combined.