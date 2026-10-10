# Lesson 11 — Workflow State Updates

## 1. Objective

Understand how workflow steps update state, preserve existing fields, and avoid accidentally discarding information.

## 2. The initial state

Our workflow begins with:

```python
{
    "pr_number": 47,
    "title": "Improve login validation",
    "status": "pending",
    "reviewer": "Alex",
}
```

Each field represents information that later workflow steps may need.

## 3. Updating one field while preserving state

The correct implementation is:

```python
def complete_review(state: ReviewState) -> ReviewState:
    return {
        **state,
        "status": "completed",
    }
```

The `**state` expression copies the existing key-value pairs into a new dictionary. The later `"status"` entry overrides the previous status.

The returned state retains `pr_number`, `title`, and `reviewer`.

## 4. What happens when we omit `**state`?

Consider this incorrect implementation:

```python
def complete_review(state: ReviewState) -> ReviewState:
    return {
        "status": "completed",
    }
```

The returned dictionary contains only the status field. The other fields disappear from the returned state.

The original dictionary remains unchanged because this function creates a new dictionary rather than mutating the input.

## 5. Original state versus updated state

Our experiment demonstrates:

- Original state: `status` remains `"pending"`.
- Updated state: `status` becomes `"completed"`.
- Both dictionaries contain the other original fields when state is preserved correctly.

Dictionary unpacking makes a shallow copy. Nested mutable objects may still be shared between the original and returned dictionaries.

## 6. Automated tests

Run the full suite from the repository root:

```bash
python -m unittest discover -s 00-python-workflows/tests -v
```

Expected result: 16 tests pass.

The three new tests verify status updates, preservation of existing fields, and preservation of the original input state.

## 7. Key takeaways

1. A plain Python function returning a dictionary does not automatically merge it with the input state.
2. Use `**state` when constructing a new dictionary that should preserve existing fields.
3. Later dictionary entries override earlier entries with the same key.
4. Returning a new dictionary does not mutate the original dictionary at the top level.
5. Automated tests can catch accidental state loss.

## 8. Connection to LangGraph

In plain Python, our function returns a complete updated dictionary to the caller.

In LangGraph, a node can return a partial state update, and the graph applies it to the shared state according to the state schema and reducer configuration.

This distinction is fundamental to understanding LangGraph nodes, state updates, and reducers.

## 9. Exercises

1. Add a `reviewer` update while preserving every other field.
2. Write a test that ensures `title` remains unchanged after completing the review.
3. Remove `**state` again and observe which tests fail.
4. Explain why this example uses a new dictionary rather than mutating the input.

## 10. References

- [Python documentation — Dictionary displays](https://docs.python.org/3/reference/expressions.html#dictionary-displays)
- [Python documentation — TypedDict](https://docs.python.org/3/library/typing.html#typing.TypedDict)
- [LangGraph — Official documentation](https://docs.langchain.com/oss/python/langgraph/overview)
