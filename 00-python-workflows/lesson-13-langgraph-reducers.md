
# Lesson 13 — LangGraph State Reducers

## Objective

Understand how LangGraph uses reducers to control how updates to individual state fields are merged.

## 1. Define the state

```python
import operator
from typing import Annotated, TypedDict


class ReviewState(TypedDict):
    findings: Annotated[list[str], operator.add]
```

- `TypedDict` defines the expected state structure.
- `list[str]` declares a list of string findings.
- `Annotated` attaches reducer metadata to the field.
- `operator.add` concatenates lists.

## 2. Define the nodes

The security review returns:

```python
{"findings": ["SQL injection risk"]}
```

The test review returns:

```python
{"findings": ["Missing test coverage"]}
```

Each node returns a partial state update. Neither needs to construct the entire state dictionary.

## 3. Understand the merge

Suppose the existing findings are:

```python
["SQL injection risk"]
```

The incoming update is:

```python
{"findings": ["Missing test coverage"]}
```

Because `findings` has the `operator.add` reducer, LangGraph combines the existing and incoming lists:

```python
["SQL injection risk", "Missing test coverage"]
```

## 4. What happens without a reducer?

Without reducer metadata:

```python
class ReviewState(TypedDict):
    findings: list[str]
```

LangGraph uses its default behavior for that field: the incoming value replaces the existing value.

In our sequential experiment, this meant the final list contained only the test finding.

## 5. Graph structure

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

The nodes run sequentially in this lesson. Parallel execution will be explored separately.

## 6. Run the example

From the repository root:

```bash
uv run python 00-python-workflows/langgraph_reducer_workflow.py
```

Expected output:

```text
Final findings: ['SQL injection risk', 'Missing test coverage']
```

## 7. Run the tests

```bash
uv run python -m unittest discover -s 00-python-workflows/tests -v
```

The complete test suite should pass, including the tests that verify reducer behavior and preservation of initial findings.

## 8. Exercises

1. Add a third node that returns a performance finding.
2. Change the initial findings and predict the final result.
3. Replace `operator.add` with a custom reducer and describe its behavior.
4. Explain why a reducer applies to a specific state field rather than automatically merging every field.

## Key takeaway

A LangGraph reducer defines how updates to a particular state field are combined with its existing value. Reducers are essential when workflow steps contribute to shared, accumulated data.
```

Save the file. Then run:

```bash
ls -l 00-python-workflows/lesson-13-langgraph-reducers.md
```

Share the output. We'll verify the documentation before checking the three Lesson 13 implementation and test files for Git.