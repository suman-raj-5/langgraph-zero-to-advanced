# Lesson 05 — Workflow State and Data Contracts

## Learning objectives

By the end of this lesson, you will understand:

- Why workflow state needs a predictable structure.
- How to declare a state schema using `TypedDict`.
- How to validate data at runtime.
- Why type annotations alone do not enforce runtime correctness.
- How to reject missing fields, incorrect types, and invalid values.

## 1. What is workflow state?

Workflow state is the data that moves through a workflow as its steps execute.

In our pull request review example, the state contains:

- `pr_number`: pull request number.
- `title`: pull request title.
- `files_changed`: number of changed files.
- `status`: current review status.

The initial state is a Python dictionary.

## 2. What is a data contract?

A data contract describes the structure and constraints that data must satisfy.

For example, a review state requires a valid integer pull request number, a non-empty title, a non-negative file count, and an allowed status.

Without a contract, a downstream step might receive missing fields or unexpected values and fail in confusing ways.

## 3. TypedDict

The `ReviewState` definition describes the expected state structure:

```python
from typing import TypedDict


class ReviewState(TypedDict):
    pr_number: int
    title: str
    files_changed: int
    status: str
```

`TypedDict` helps IDEs and static type checkers detect many mistakes before execution.

**Important:** `TypedDict` does not automatically validate values at runtime. A dictionary with an incorrect value can still be created and passed around by Python.

## 4. Runtime validation

The `validate_state()` function checks:

1. Required keys are present.
2. `pr_number` is an integer, excluding booleans.
3. `title` is a non-empty string.
4. `files_changed` is an integer, excluding booleans.
5. `files_changed` is not negative.
6. `status` is one of `pending`, `completed`, or `failed`.

Invalid data raises `ValueError`.

Validating state at workflow boundaries helps prevent downstream steps from relying on incorrect assumptions.

## 5. Experiments performed

### Experiment A — Valid state

The original state passes validation.

### Experiment B — Negative file count

Setting `files_changed` to `-3` raises:

```text
ValueError: files_changed cannot be negative
```

### Experiment C — Incorrect type

Setting `pr_number` to `"forty-two"` raises:

```text
ValueError: pr_number must be an integer
```

### Experiment D — Missing field

Removing `files_changed` raises:

```text
ValueError: Missing required keys: ['files_changed']
```

### Experiment E — TypedDict at runtime

A dictionary containing `"pr_number": "forty-two"` can still be created and printed without a runtime validation error if `validate_state()` is not called.

This demonstrates the difference between static typing and runtime validation.

## 6. Run the lesson

From the repository root:

```bash
python 00-python-workflows/state_workflow.py
```

Expected output:

```text
State is valid:
{'pr_number': 42, 'title': 'Fix authentication validation', 'files_changed': 3, 'status': 'pending'}
```

No external API or additional dependency is required.

## 7. Exercises

1. Add a required `author` field to the state.
2. Update `receive_pull_request()` and `validate_state()` to support it.
3. What happens if `files_changed` is `True`? Why does the validator explicitly exclude booleans?
4. Why is `TypedDict` not a replacement for runtime validation?
5. What would change if the workflow received data from an external API instead of constructing the dictionary itself?

## 8. Connection to LangGraph

LangGraph workflows use state schemas to describe the data shared between nodes. Understanding `TypedDict` and runtime validation now will make it easier to understand graph state, state updates, reducers, and node boundaries later.

This lesson uses plain Python; LangGraph has not yet been introduced.

## 9. References

- [Python documentation — TypedDict](https://docs.python.org/3/library/typing.html#typing.TypedDict)
- [Python documentation — Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
- [Python typing documentation](https://docs.python.org/3/library/typing.html)
