
# Lesson 15 — Reducers with Parallel Branches

## Objective

Understand how parallel LangGraph nodes contribute updates to a shared state field and how a custom reducer merges those updates.

## 1. Graph structure

```text
             START
             /   \
            v     v
     Security     Test
      Review      Review
            \     /
             v   v
              END
```

Both branches are connected directly to `START`:

```python
graph.add_edge(START, "security_review")
graph.add_edge(START, "test_review")
```

LangGraph can schedule both branches in the same execution step.

## 2. Shared state

Both nodes return updates to the same field:

```python
class ReviewState(TypedDict):
    findings: Annotated[list[str], merge_unique_findings]
```

The security review returns:

```python
{
    "findings": [
        "SQL injection risk",
        "Hardcoded secret",
    ]
}
```

The test review returns:

```python
{
    "findings": [
        "Missing test coverage",
        "Hardcoded secret",
    ]
}
```

## 3. How the reducer helps

Both branches report `"Hardcoded secret"`.

The custom reducer combines the updates and removes exact duplicates. The final state contains these three distinct findings:

- SQL injection risk
- Hardcoded secret
- Missing test coverage

## 4. Parallel execution and ordering

Parallel branch execution does not guarantee a fixed completion order.

Therefore, tests should not assume a specific order for the merged list unless the workflow explicitly guarantees one.

The tests in this lesson compare the set of findings and check the number of entries. Together, these checks verify that all expected findings are present and no duplicates remain.

## 5. Initial state preservation

The reducer also preserves findings that were already present before the branches ran.

For example, an initial finding called `"Existing finding"` remains in the final result alongside the findings from both branches.

## 6. Run the example

```bash
uv run python 00-python-workflows/parallel_reducer_workflow.py
```

## 7. Run the tests

```bash
uv run python -m unittest discover -s 00-python-workflows/tests -v
```

The complete test suite should pass, including both parallel reducer tests.

## 8. Exercises

1. Add a third parallel branch for performance review.
2. Make two branches report the same finding and verify that only one copy remains.
3. Explain why list ordering can be unreliable when parallel branches contribute updates.
4. What could go wrong if the reducer simply concatenated every incoming list?
5. What would change if each branch wrote to a separate state key?

## Key takeaway

Reducers define how updates to a shared state field are merged. They become particularly important when multiple parallel branches contribute to the same field.
```

Save the file, then run:

```bash
ls -l 00-python-workflows/lesson-15-parallel-reducers.md
git status --short
```

Share the output. We'll verify the documentation and stage only the intended Lesson 15 files.