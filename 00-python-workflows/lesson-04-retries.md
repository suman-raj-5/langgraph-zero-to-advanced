# Lesson 04 — Error Handling and Retries in Python

## Learning objectives

By the end of this lesson, you will understand how to:

- Handle expected errors with `try` and `except`.
- Retry a failed operation using a bounded loop.
- Track workflow progress and errors in state.
- Stop retrying when an operation succeeds.
- Terminate safely when the maximum number of attempts is reached.

## 1. Why retries matter

Real-world workflows depend on operations that can fail temporarily, such as network requests, API calls, and database connections.

A workflow that stops after every temporary failure can be unnecessarily fragile. Retrying a suitable operation can improve reliability.

However, retries should be bounded. An operation that never succeeds must not cause an infinite loop.

## 2. How the workflow works

The implementation is in `retry_workflow.py`.

1. Initialize the workflow state.
2. Increment the attempt counter.
3. Call the simulated service inside a `try` block.
4. Catch an expected `ConnectionError`.
5. Retry while attempts remain.
6. Store the result and stop immediately on success.
7. Mark the workflow as `failed` if every allowed attempt fails.

## 3. Important Python concepts

### `try` and `except`

The `try` block contains an operation that may raise an exception. The `except ConnectionError` block handles that specific error.

Catching a specific exception is preferable to catching every exception indiscriminately.

### Bounded retries

The loop condition:

```python
while state["attempt"] < state["max_attempts"]:
```

ensures that the workflow cannot exceed its configured attempt limit.

### `break`

After success, `break` exits the loop immediately. The workflow does not waste additional attempts.

### State tracking

The state records:

- `attempt`: number of attempts made.
- `max_attempts`: maximum permitted attempts.
- `status`: `pending`, `completed`, or `failed`.
- `result`: successful output, or `None` if unsuccessful.
- `error`: most recently caught error, or `None` after success.

## 4. Experiments performed

### Experiment A — Successful retry

The simulated service fails on attempts 1 and 2 and succeeds on attempt 3.

Expected final state:

```python
{
    "attempt": 3,
    "max_attempts": 5,
    "status": "completed",
    "result": "Review data received successfully",
    "error": None,
}
```

### Experiment B — Retry exhaustion

Temporarily change `if attempt < 3:` to `if attempt < 10:`.

The service then fails on all five permitted attempts.

Expected final state:

```python
{
    "attempt": 5,
    "max_attempts": 5,
    "status": "failed",
    "result": None,
    "error": "Temporary service failure",
}
```

After the experiment, restore `if attempt < 3:` and verify the successful path again.

## 5. Run the lesson

From the repository root:

```bash
python 00-python-workflows/retry_workflow.py
```

No API key or external service is required.

## 6. Exercises

1. Change the simulation so that the service succeeds on attempt 4. What should the final `attempt` value be?
2. Set `max_attempts=2`. What should happen when the service still fails on attempts 1 and 2?
3. Why should the workflow stop immediately after success?
4. Why is `ConnectionError` a more appropriate exception to catch here than a bare `except:`?
5. What could go wrong if a retried operation creates a payment or submits a non-idempotent request?

## 7. Production considerations

This lesson demonstrates the core retry pattern, not a complete production retry system.

Production systems may also need:

- Timeouts and exponential backoff.
- A distinction between transient and permanent errors.
- Structured logging and observability.
- Idempotency safeguards for operations with side effects.
- Retry policies with explicit limits.

A retry should not blindly repeat every failed operation.

## 8. Connection to LangGraph

LangGraph provides graph-level retry policies for eligible node failures. Learning retries in plain Python first makes it easier to understand what a framework retry policy automates and how failures affect workflow execution.

This lesson uses a manual retry loop; it does not yet use LangGraph.

## 9. References

- [Python — Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
- [Python — Built-in Exceptions](https://docs.python.org/3/library/exceptions.html)
- [LangGraph — Official documentation](https://docs.langchain.com/oss/python/langgraph/overview)
