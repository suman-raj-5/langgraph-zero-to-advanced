# Lesson 24 — LangGraph Send with Custom Worker State

## Learning objectives

By the end of this lesson, you should understand how to:

- Use `Send` to dispatch individual tasks to dynamically created worker executions.
- Pass task-specific input to each worker.
- Distinguish the parent graph's state from a worker's input.
- Collect worker results using a state reducer.
- Test dynamic fan-out, including an empty task list.

## 1. The problem

Imagine reviewing a pull request containing several files. Each file may need a different review category, such as security or SQL.

A single shared state describes the overall workflow, but each worker needs its own file, content, and review category.

We can use `Send` to provide a separate input payload to each worker.

## 2. Parent state versus worker state

The parent graph uses `ReviewState`:

```python
class ReviewState(TypedDict):
    tasks: list[dict[str, str]]
    findings: Annotated[list[str], operator.add]
```

- `tasks` contains the work to distribute.
- `findings` collects results from workers.
- `operator.add` combines finding lists returned by different workers.

Each worker receives a `ReviewTask`:

```python
class ReviewTask(TypedDict):
    file: str
    content: str
    category: str
```

The worker receives one task, not the entire parent state.

## 3. Dynamic dispatch with Send

```python
def dispatch_reviews(state: ReviewState) -> list[Send]:
    return [
        Send("review_file", task)
        for task in state["tasks"]
    ]
```

For every task, `Send` specifies:

1. The destination node: `"review_file"`.
2. The input payload: that task's dictionary.

If the parent contains three tasks, this routing function creates three worker dispatches.

## 4. Processing each task

```python
def review_file(task: ReviewTask) -> dict:
    file = task["file"]
    content = task["content"]
    category = task["category"]

    finding = (
        f"{category} review of {file}: "
        f"{len(content)} characters examined"
    )

    return {"findings": [finding]}
```

The worker reads its own task payload and returns a partial state update.

It returns a list containing one finding because the parent state defines `findings` as a list.

## 5. Building the graph

```python
def build_graph():
    graph = StateGraph(ReviewState)

    graph.add_node("review_file", review_file)
    graph.add_conditional_edges(START, dispatch_reviews)
    graph.add_edge("review_file", END)

    return graph.compile()
```

The routing function dynamically dispatches tasks from `START`. Each worker processes its assigned task and reaches `END`.

The reducer combines the worker findings into the final parent state.

## 6. Run the lesson

```bash
uv run python 00-python-workflows/langgraph_send_custom_state_workflow.py
```

Expected findings:

```text
security review of auth.py: 17 characters examined
SQL review of database.py: 19 characters examined
```

Worker execution order is not guaranteed when tasks execute in parallel. The final findings may therefore appear in a different order.

## 7. Run the tests

Run the focused tests:

```bash
uv run python -m unittest discover -s 00-python-workflows/tests -p "test_langgraph_send_custom_state_workflow.py" -v
```

Run the complete regression suite:

```bash
uv run python -m unittest discover -s 00-python-workflows/tests -v
```

The focused tests verify that workers use their own task inputs and that an empty task list produces no findings.

## 8. Exercises

1. Add a third task for `api.py` with category `"API"`. Verify that its finding appears.
2. Add a `severity` field to `ReviewTask` and include it in the finding.
3. Explain why the worker receives `ReviewTask` rather than the complete `ReviewState`.
4. What would happen if multiple workers updated `findings` without a reducer?
5. Why should tests avoid assuming a particular order for parallel results?

## Key takeaway

**`Send` separates dynamic task dispatch from shared workflow state.** Each worker receives its own task-specific input, while reducers combine the workers' partial results into the parent graph's final state.

The parent state describes the workflow; the worker payload describes one unit of work.
