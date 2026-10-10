# Lesson 06 — Shared State and Workflow Steps

## Learning objectives

By the end of this lesson, you will understand how to:

- Pass state between sequential workflow steps.
- Preserve existing fields while adding new information.
- Update an existing field without losing unrelated data.
- Describe evolving workflow state with `TypedDict` and `NotRequired`.
- Understand the difference between plain Python state updates and LangGraph state updates.

## 1. What is shared workflow state?

Workflow state is the information that flows between steps.

In this pull request review example, the state contains:

- `pr_number`: pull request number.
- `title`: pull request title.
- `files_changed`: number of changed files.
- `status`: current review status.
- `inspection_result`: inspection output.
- `summary`: generated summary.

Each step receives the state produced by the previous step.

## 2. The workflow sequence

The workflow follows this sequence:

1. `receive_pull_request()` creates the initial state.
2. `inspect_changes()` adds `inspection_result`.
3. `generate_summary()` adds `summary`.
4. `complete_review()` changes `status` to `completed`.

The final state retains information produced by every step.

## 3. Preserving state with dictionary unpacking

This pattern preserves existing top-level fields while adding a new field:

```python
return {
    **state,
    "inspection_result": "Changes inspected successfully",
}
```

The `**state` expression copies the existing key-value pairs into a new dictionary. The new field is then added.

If the unpacking is omitted, the function returns only the fields explicitly included in the new dictionary. Downstream steps may then fail because required fields have disappeared.

This is a shallow copy: nested mutable objects are not recursively copied.

## 4. Updating an existing field

The `complete_review()` step uses:

```python
return {
    **state,
    "status": "completed",
}
```

Because the new `"status"` entry appears after `**state`, it replaces the previous value of that key.

All other top-level fields are preserved.

## 5. Describing evolving state with TypedDict

The state schema uses `TypedDict` to describe expected fields:

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

The inspection result and summary are optional because they are added later in the workflow.

`NotRequired[str]` means that a key may be absent. If present, its value should be a string.

`TypedDict` is primarily for static type checking. It does not automatically enforce these constraints at runtime.

## 6. Run the lesson

From the repository root:

```bash
python 00-python-workflows/shared_state_workflow.py
```

Expected behavior:

- The initial state has the PR details and `status: pending`.
- The inspection step adds `inspection_result`.
- The summary step adds `summary`.
- The final step changes `status` to `completed`.
- All previously produced fields remain in the final state.

No external API or additional dependency is required.

## 7. Experiments performed

### Experiment A — Preserve state

The workflow retains all existing fields as new information is added.

### Experiment B — Deliberately discard state

Removing `**state` from `inspect_changes()` causes the original PR fields to disappear. The summary step then raises `KeyError` when it attempts to access `pr_number`.

Restoring `**state` fixes the failure.

### Experiment C — Update status

The final step changes `status` from `pending` to `completed` while preserving the rest of the state.

## 8. Exercises

1. Add a `reviewer` field to the initial state and preserve it through every step.
2. Add a new step that changes the status to `failed` without losing other fields.
3. What happens if a later dictionary entry uses the same key as an earlier entry?
4. Why is `**state` a shallow copy rather than a deep copy?
5. How is returning a complete dictionary in plain Python different from returning a partial state update in LangGraph?

## 9. Connection to LangGraph

LangGraph nodes commonly read graph state and return state updates. The graph applies those updates according to its schema and reducer behavior.

This lesson establishes the state-flow concepts needed to understand nodes, graph state updates, reducers, and partial updates in LangGraph.

This implementation uses plain Python; LangGraph has not yet been introduced.

## 10. References

- [Python documentation — TypedDict](https://docs.python.org/3/library/typing.html#typing.TypedDict)
- [Python documentation — Dictionary displays](https://docs.python.org/3/reference/expressions.html#dictionary-displays)
- [LangGraph — Official documentation](https://docs.langchain.com/oss/python/langgraph/overview)
