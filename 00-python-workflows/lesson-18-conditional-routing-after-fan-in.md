# Lesson 18 — Conditional Routing After Fan-in

## Objective

Learn how to combine results from parallel branches, synchronize execution with a fan-in edge, and choose the next node using conditional routing.

## 1. Graph structure

```text
                  START
                  /   \
                 v     v
          Security    Test
           Review    Review
                 \   /
                  v v
             Combine Reviews
                    |
                    v
             Security findings?
                /       \
              Yes        No
               |          |
               v          v
        Remediation    Final Report
               \          /
                    END
```

## 2. Parallel review branches

Both review nodes start independently:

```python
graph.add_edge(START, "security_review")
graph.add_edge(START, "test_review")
```

Each branch contributes findings and records its completion.

## 3. Fan-in synchronization

The combined review node waits for both branches:

```python
graph.add_edge(
    ["security_review", "test_review"],
    "combine_reviews",
)
```

The reducers merge the list updates, while the fan-in edge controls when `combine_reviews` executes.

## 4. Conditional routing

The routing function examines the combined findings:

```python
def route_after_reviews(state: ReviewState):
    has_security_finding = any(
        "security" in finding.lower()
        or "sql injection" in finding.lower()
        or "hardcoded secret" in finding.lower()
        for finding in state["findings"]
    )

    if has_security_finding:
        return "remediation"

    return "final_report"
```

The graph maps the routing result to a destination:

```python
graph.add_conditional_edges(
    "combine_reviews",
    route_after_reviews,
    {
        "remediation": "remediation",
        "final_report": "final_report",
    },
)
```

The routing function returns a destination label. The mapping tells LangGraph which node to execute.

## 5. Expected behavior

The example produces three unique findings:

- SQL injection risk
- Hardcoded secret
- Missing test coverage

Because the combined findings include security-related risks, the graph selects the remediation path.

The example's remediation node marks remediation as required. It does not automatically modify or fix source code.

## 6. Run the workflow

```bash
uv run python 00-python-workflows/langgraph_conditional_fan_in_workflow.py
```

## 7. Run the lesson tests

```bash
uv run python -m unittest 00-python-workflows/tests/test_langgraph_conditional_fan_in_workflow.py -v
```

Run the full test suite:

```bash
uv run python -m unittest discover -s 00-python-workflows/tests -v
```

The full suite passed with 40 tests when this lesson was verified.

## 8. Exercises

1. What would happen if both review branches found no security-related risks?
2. Why should routing occur after fan-in rather than before the results are combined?
3. What is the difference between a conditional edge and a normal edge?
4. Why does the routing function use `finding.lower()`?
5. How would you change the graph to route critical findings to a human approval node?

## Key takeaway

Parallel branches gather information, fan-in ensures the combined state is ready, and conditional routing chooses the next action based on that state. This pattern is useful for code review, validation pipelines, and agent workflows.