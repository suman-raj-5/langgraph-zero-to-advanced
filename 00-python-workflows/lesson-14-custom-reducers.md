
# Lesson 14 — Custom State Reducers

## Objective

Build a custom reducer that combines findings, removes exact duplicates, and preserves first-seen order. Integrate it into a LangGraph state field.

## 1. Why do we need a custom reducer?

The built-in `operator.add` reducer concatenates lists, including duplicate entries.

For example:

```python
existing = ["SQL injection", "Missing tests"]
incoming = ["Missing tests", "Hardcoded secret"]
```

Simple concatenation produces a duplicate `"Missing tests"` entry.

For a code-review workflow, we want each exact finding to appear only once.

## 2. Implement the reducer

```python
def merge_unique_findings(
    existing: list[str],
    incoming: list[str],
) -> list[str]:
    merged = []
    seen = set()

    for finding in existing + incoming:
        if finding not in seen:
            merged.append(finding)
            seen.add(finding)

    return merged
```

### How it works

- `existing + incoming` creates a combined list without modifying the input lists.
- `seen` tracks findings already processed.
- `merged` preserves the order of each finding's first occurrence.
- The function returns a new list.

This implementation removes exact string duplicates. It is case-sensitive, so `"Missing tests"` and `"missing tests"` remain distinct.

## 3. Register it with LangGraph

```python
from typing import Annotated, TypedDict

class ReviewState(TypedDict):
    findings: Annotated[list[str], merge_unique_findings]
```

`Annotated` attaches the custom reducer to the `findings` field.

When a node returns a `findings` update, LangGraph invokes the reducer to combine the existing value with the incoming value.

## 4. Graph structure

```text
START
  |
  v
Security Review
  |
  v
Test Review
  |
  v
END
```

The security node returns:

```python
{"findings": ["SQL injection", "Missing tests"]}
```

The test node returns:

```python
{"findings": ["Missing tests", "Hardcoded secret"]}
```

Starting with an empty findings list, the final result is:

```python
["SQL injection", "Missing tests", "Hardcoded secret"]
```

## 5. Run the example

From the repository root:

```bash
uv run python 00-python-workflows/custom_reducer_workflow.py
```

Expected output:

```text
Final findings: ['SQL injection', 'Missing tests', 'Hardcoded secret']
```

## 6. Run the tests

```bash
uv run python -m unittest discover -s 00-python-workflows/tests -v
```

The complete test suite should pass, including tests for duplicate removal, ordering, empty inputs, input immutability, and LangGraph integration.

## 7. Exercises

1. Make duplicate detection case-insensitive.
2. Explain the difference between `operator.add` and `merge_unique_findings`.
3. Add a third node that returns findings already reported by the first two nodes.
4. Consider whether two differently worded findings might describe the same underlying issue. Why is exact string deduplication insufficient for that problem?

## Key takeaway

A custom reducer lets you define domain-specific merge behavior for a LangGraph state field. Choose the merge rule based on the meaning of the data, not merely its Python type.
```

Save the file, then run:

```bash
ls -l 00-python-workflows/lesson-14-custom-reducers.md
```

Share the output. We'll verify the documentation and then stage only the intended Lesson 14 files.