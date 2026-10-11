# Lesson 16 — Parallel State Updates Without a Reducer

## Objective

Understand why LangGraph raises `InvalidUpdateError` when multiple parallel nodes update the same state key without a reducer, and learn how a reducer resolves the conflict.

## 1. The graph

Two branches start in the same execution step:

```text
             START
             /   \
            v     v
       Security    Test
        Review    Review
            \      /
             v    v
              END
```

Both branches update the `findings` field.

## 2. State without a reducer

The original state declaration was:

```python
class ReviewState(TypedDict):
    findings: list[str]
```

The type annotation says that `findings` contains strings in a list. It does not specify how multiple concurrent updates should be merged.

## 3. The error

Running the graph without a reducer produced:

```text
InvalidUpdateError: At key 'findings':
Can receive only one value per step.
Use an Annotated key to handle multiple values.
```

Both nodes ran, but LangGraph could not apply both updates to the same last-value channel in one step.

## 4. Fixing the conflict

We changed the state declaration to:

```python
from typing import Annotated, TypedDict

from custom_reducer_workflow import merge_unique_findings


class ReviewState(TypedDict):
    findings: Annotated[list[str], merge_unique_findings]
```

The reducer defines how concurrent updates are combined. In this example, it merges the findings and removes exact duplicates while preserving first-seen order.

## 5. Expected result

The workflow produces these findings:

- SQL injection risk
- Hardcoded secret
- Missing test coverage

Both branches contribute their findings, and the duplicate `Hardcoded secret` appears only once.

## 6. Tests

The lesson tests verify that:

1. Both parallel branches contribute their findings.
2. Duplicate findings are removed.
3. Findings already present in the initial state are preserved.

Run the example:

```bash
uv run python 00-python-workflows/parallel_without_reducer_workflow.py
```

Run the lesson tests:

```bash
uv run python -m unittest 00-python-workflows/tests/test_parallel_without_reducer_workflow.py -v
```

Run the complete test suite:

```bash
uv run python -m unittest discover -s 00-python-workflows/tests -v
```

The complete suite passed with 35 tests at the time this lesson was verified.

## 7. Exercises

1. What is the difference between `list[str]` and `Annotated[list[str], merge_unique_findings]`?
2. Why can two parallel nodes not independently write to the same default last-value channel in one step?
3. What would happen if both branches wrote to separate state keys instead?
4. When might concatenation be more appropriate than deduplication?
5. Why should tests avoid assuming a fixed order for findings returned by parallel branches?

## Key takeaway

A state type describes the shape of a value; a reducer defines how updates to that state field are combined. When parallel nodes write to the same field, choose a reducer whose behavior matches the workflow's requirements.