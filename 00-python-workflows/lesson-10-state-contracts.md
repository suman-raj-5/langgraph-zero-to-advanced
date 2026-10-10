# Lesson 10 — Workflow State Contracts

## 1. Objective

Learn how to define workflow state with `TypedDict`, distinguish required and optional fields, and validate data at runtime.

## 2. What is a state contract?

A state contract describes the structure and expected types of data passed between workflow steps.

Our `ReviewState` contract defines:
- `pr_number`: integer
- `title`: string
- `files_changed`: integer
- `status`: string
- `inspection_result`: optional string
- `summary`: optional string

## 3. TypedDict

Python's `TypedDict` describes the expected keys and value types of a dictionary for static type checking.

```python
from typing import TypedDict

class ReviewState(TypedDict):
    pr_number: int
    title: str
    files_changed: int
    status: str
```

Important: `TypedDict` does not automatically validate actual dictionary values at runtime.

## 4. Required and optional fields

We use `NotRequired` for fields that need not exist in every state:

```python
from typing import NotRequired, TypedDict

class ReviewState(TypedDict):
    pr_number: int
    title: str
    files_changed: int
    status: str
    inspection_result: NotRequired[str]
    summary: NotRequired[str]
```

The initial state can omit `inspection_result` and `summary`. Later workflow steps can add them.

## 5. Runtime validation

The `validate_state()` function explicitly checks:
- Required fields are present.
- `pr_number` is an integer, not a boolean.
- `title` is a non-empty string.
- `files_changed` is an integer, not a boolean.
- `files_changed` is non-negative.
- `status` is one of `pending`, `completed`, or `failed`.

Invalid state raises `ValueError`.

## 6. Why reject booleans for integer fields?

In Python, `bool` is a subclass of `int`. Therefore, `isinstance(True, int)` returns `True`.

For a pull-request number or file count, accepting `True` as an integer would be misleading. Our validator explicitly excludes booleans.

## 7. Run the tests

From the repository root:

```bash
python -m unittest discover -s 00-python-workflows/tests -v
```

Expected result: 13 tests pass.

The suite covers state contracts, validation failures, reusable workflow composition, and fan-out/fan-in behavior.

## 8. Key takeaways

- `TypedDict` describes dictionary structure for static type checking.
- `NotRequired` identifies fields that may be absent.
- Runtime validation checks actual values.
- Type checks and business rules are separate concerns.
- Automated tests protect both valid behavior and failure cases.

These concepts prepare us for LangGraph, where a shared state schema describes the data available to graph nodes.

## 9. Reference

- [Python documentation — TypedDict](https://docs.python.org/3/library/typing.html#typing.TypedDict)
