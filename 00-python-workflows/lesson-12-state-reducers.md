
# Lesson 12 — State Reducers

## Objective

Understand how workflow updates are combined, why ordinary assignment can lose data, and how a reducer defines a merge rule.

## 1. The problem

Suppose a pull-request review has two independent steps:

- Security review produces `["SQL injection risk"]`.
- Test review produces `["Missing test coverage"]`.

This code loses the security finding:

```python
findings = security_findings
findings = test_findings
```

The second assignment replaces the first value.

## 2. Define a reducer

A reducer is a function that combines an existing value with an incoming value.

In this lesson, the reducer combines lists:

```python
def merge_findings(
    existing: list[str],
    incoming: list[str],
) -> list[str]:
    return existing + incoming
```

Example:

```python
merge_findings(
    ["SQL injection risk"],
    ["Missing test coverage"],
)
```

Result:

```python
["SQL injection risk", "Missing test coverage"]
```

## 3. Important properties

- Both sets of findings are preserved.
- The existing items appear before incoming items.
- Empty lists are supported.
- The function returns a new list without mutating either input.

## 4. Why reducers matter

When multiple workflow branches contribute updates to the same state field, a defined merge rule helps combine their results instead of simply replacing one result with another.

Reducers are particularly useful for findings, messages, collected results, and other accumulated state.

## 5. Plain Python versus LangGraph

In this lesson, we call `merge_findings()` explicitly.

LangGraph allows a reducer to be associated with a state field. When that field receives an update, LangGraph uses the reducer to combine the update with the existing value.

The exact behavior depends on the reducer configured for that field.

## 6. Tests

Run the complete test suite from the repository root:

```bash
python -m unittest discover -s 00-python-workflows/tests -v
```

The reducer tests cover combining lists, empty inputs, ordering, and input immutability.

## 7. Exercises

1. Write a reducer that combines two lists of file paths.
2. What happens if the same finding appears in both lists?
3. Modify a reducer to remove duplicate findings while preserving their first-seen order.
4. Explain why ordinary assignment is different from a merge operation.

## Key takeaway

A reducer defines how an incoming update is combined with an existing value. In LangGraph, reducers make state-update behavior explicit for individual state fields.
