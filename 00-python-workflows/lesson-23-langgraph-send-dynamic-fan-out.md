
# Lesson 23 — LangGraph Send and Dynamic Fan-Out

## Objective

Learn how to use LangGraph's `Send` to dynamically dispatch work to the same node with different inputs, and collect results using a state reducer.

## 1. The problem

A pull request may change a variable number of files. We want to review each file without creating a separate graph node for every file.

`Send` allows a routing function to create tasks dynamically based on the current state.

## 2. Workflow structure

```text
START
  |
  v
dispatch_reviews
  |
  +---- Send("review_file", {"file": "auth.py"})
  |
  +---- Send("review_file", {"file": "database.py"})
  |
  +---- Send("review_file", {"file": "api.py"})
  |
  v
review_file workers
  |
  v
END
```

Each `Send` targets the same worker node but supplies a different task input.

## 3. Dispatch with Send

```python
from langgraph.types import Send


def dispatch_reviews(state: ReviewState) -> list[Send]:
    return [
        Send("review_file", {"file": file})
        for file in state["files"]
    ]
```

The number of tasks depends on the number of files in the input state.

## 4. Worker-specific input

```python
class FileReviewState(TypedDict):
    file: str


def review_file(state: FileReviewState) -> dict:
    file = state["file"]
    return {"findings": [f"Reviewed {file}"]}
```

The worker receives its task-specific input rather than needing the entire parent state.

## 5. Collecting parallel results

```python
import operator
from typing import Annotated


class ReviewState(TypedDict):
    files: list[str]
    findings: Annotated[list[str], operator.add]
```

The `operator.add` reducer combines the lists returned by the workers.

Parallel execution does not guarantee that results will appear in the same order as the input files. Tests should avoid depending on ordering unless the workflow explicitly enforces it.

## 6. Empty input

When `files` is empty, the dispatcher returns an empty list of `Send` tasks. No file-review workers run, and the initial empty findings list remains empty.

## 7. Run the workflow

```bash
uv run python 00-python-workflows/langgraph_send_workflow.py
```

The example reviews three files and collects three findings.

## 8. Run the tests

Run this lesson's tests:

```bash
uv run python -m unittest 00-python-workflows/tests/test_langgraph_send_workflow.py -v
```

Run the complete suite:

```bash
uv run python -m unittest discover -s 00-python-workflows/tests -v
```

The complete suite passed with 52 tests during verification.

## 9. Exercises

1. What does `Send` specify?
2. Why can one worker node process a variable number of files?
3. Why does the parent state use `Annotated[list[str], operator.add]`?
4. What happens when the input file list is empty?
5. Why shouldn't a test assume parallel findings always preserve input order?
6. How could you attach a file identifier to each result so results can be correlated reliably?

## Key takeaway

`Send` enables dynamic fan-out by dispatching multiple tasks to a node with different inputs. Reducers combine the workers' updates, allowing a graph to process a variable amount of work without defining a separate node for every item.
