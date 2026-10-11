# Lesson 25 — LangGraph Map-Reduce with Send

## Learning objectives

By the end of this lesson, you should understand how to:

- Use `Send` for dynamic fan-out.
- Give each worker its own task-specific input.
- Collect parallel results with a state reducer.
- Aggregate collected results in a dedicated reduce-stage node.
- Handle empty input explicitly.
- Test successful execution, empty input, and input-state immutability.

## 1. What is map-reduce?

Map-reduce divides a larger task into independent units of work and combines their results.

In our pull-request review example:

1. **Map:** dispatch a review task for each changed file.
2. **Worker:** inspect one file and return a finding.
3. **State reducer:** merge worker findings into a shared list.
4. **Reduce:** generate one summary after the workers finish.

## 2. State schemas

The parent graph uses `ReviewState`:

```python
class ReviewState(TypedDict):
    tasks: list[dict[str, str]]
    review_results: Annotated[list[str], operator.add]
    summary: str
```

Each worker receives a `ReviewTask`:

```python
class ReviewTask(TypedDict):
    file: str
    content: str
```

The parent state represents the overall workflow. The worker schema describes one unit of work.

## 3. Map stage: dynamic dispatch

```python
def dispatch_reviews(state: ReviewState) -> list[Send] | str:
    if not state["tasks"]:
        return "summarize_reviews"

    return [
        Send("review_file", task)
        for task in state["tasks"]
    ]
```

For every task, `Send` targets `review_file` with that task's payload.

The empty-input branch is important. If there are no tasks, the function routes directly to `summarize_reviews`. Otherwise, no worker would run and the summary would remain unchanged.

## 4. Worker stage

```python
def review_file(task: ReviewTask) -> dict:
    file = task["file"]
    content = task["content"]

    result = (
        f"Reviewed {file}: "
        f"{len(content)} characters examined"
    )

    return {"review_results": [result]}
```

Each worker returns a partial update containing a list with one result.

## 5. Collecting worker results

```python
review_results: Annotated[list[str], operator.add]
```

The reducer combines list updates from workers. Without a suitable reducer, multiple workers updating the same state key can cause an `InvalidUpdateError`.

Worker completion order is not guaranteed. Tests should avoid depending on parallel result ordering unless the workflow explicitly guarantees it.

## 6. Reduce stage

```python
def summarize_reviews(state: ReviewState) -> dict:
    results = state["review_results"]

    summary = (
        f"Review complete: {len(results)} files reviewed."
    )

    return {"summary": summary}
```

This node aggregates the collected results into a final summary.

Do not confuse the two kinds of reduction:

- `operator.add` is a **state reducer** that merges updates.
- `summarize_reviews` is a **graph node** that computes the final summary.

## 7. Graph synchronization

The graph connects `START` to `dispatch_reviews` using conditional routing. Each dispatched worker leads to `summarize_reviews`, and the summary node leads to `END`.

LangGraph schedules the dispatched workers and executes the downstream aggregation after the dispatched work completes. The empty-input route goes directly to the summary node.

## 8. Run the workflow

```bash
uv run python 00-python-workflows/langgraph_map_reduce_workflow.py
```

The example reviews three files and produces:

```text
Summary: Review complete: 3 files reviewed.
```

## 9. Run the tests

Focused tests:

```bash
uv run python -m unittest discover -s 00-python-workflows/tests -p "test_langgraph_map_reduce_workflow.py" -v
```

Full regression suite:

```bash
uv run python -m unittest discover -s 00-python-workflows/tests -v
```

The tests cover:

- Multiple tasks produce the expected review results and summary.
- Empty tasks produce an empty result list and a valid zero-file summary.
- Graph execution does not mutate the original input dictionary.

## 10. Exercises

1. Add a fourth file and verify the summary counts four results.
2. Add a `category` field to each task and include it in the finding.
3. Explain the difference between `Send`, the `operator.add` reducer, and `summarize_reviews`.
4. Explain why the empty-input route is necessary.
5. Modify the worker to return multiple findings for one file. How should the summary count files rather than individual findings?

## Key takeaway

**Map-reduce combines dynamic fan-out with result aggregation.** `Send` distributes tasks, the state reducer collects worker updates, and the reduce-stage node generates the final output. Explicitly handling empty input makes the workflow more robust.
