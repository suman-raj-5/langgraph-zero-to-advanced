
# Lesson 21 — Command, END, and Literal Destinations

## Objective

Learn how to terminate a LangGraph workflow directly with `Command(goto=END)` and use `Literal` to describe possible routing destinations for static type checking.

## 1. Workflow behavior

The review node handles two outcomes:

- Approved: update the message and route to `finish`.
- Rejected: update the message and terminate the graph directly.

```text
START
  |
  v
review_node
  |
  +-- approved --> finish_node --> END
  |
  +-- rejected -----------------> END
```

## 2. Direct termination with Command

```python
return Command(
    update={"message": "Review rejected"},
    goto=END,
)
```

This updates the message and ends graph execution without invoking another application node.

The status remains `"rejected"` because no subsequent node changes it.

## 3. Routing to another node

```python
return Command(
    update={"message": "Review approved"},
    goto="finish",
)
```

This updates the message and routes execution to `finish_node`. That node changes the status to `"completed"` before the graph ends.

## 4. Literal destination types

The example uses this return annotation:

```python
Command[Literal["finish", "__end__"]]
```

It describes the destinations the node may choose:

- `"finish"` is a named graph node.
- `"__end__"` is the internal string representation of LangGraph's `END` destination.

`Literal` helps static type checkers understand the intended destinations. It does not perform runtime routing; `Command.goto` controls the route.

## 5. Run the workflow

```bash
uv run python 00-python-workflows/langgraph_command_end_workflow.py
```

Try both initial states:

- `"status": "approved"` should produce `"completed"`.
- `"status": "rejected"` should preserve `"rejected"` and end directly.

## 6. Run the tests

Run this lesson's tests:

```bash
uv run python -m unittest 00-python-workflows/tests/test_langgraph_command_end_workflow.py -v
```

Run the complete suite:

```bash
uv run python -m unittest discover -s 00-python-workflows/tests -v
```

The full suite passed with 47 tests during verification.

## 7. Exercises

1. What is the difference between `goto="finish"` and `goto=END`?
2. Why does the rejected path preserve its original status?
3. What purpose does `Literal` serve in the return annotation?
4. Does `Literal` enforce valid destinations at runtime?
5. How would you test that a node was not executed after direct termination?

## Key takeaway

`Command(goto=END)` allows a node to terminate a workflow directly while applying its state update. `Literal` communicates intended routing destinations to static type checkers, while runtime execution is controlled by LangGraph.
