
# Lesson 20 — Command: State Updates and Routing

## Objective

Learn how LangGraph's `Command` lets a node update graph state and choose the next node in one return value.

## 1. What is Command?

A node can return a `Command` object containing:

- `update`: the state fields to update.
- `goto`: the name of the next node to execute.

Example:

```python
from langgraph.types import Command

return Command(
    update={"message": "Review approved"},
    goto="finish",
)
```

This updates `message` and directs execution to the `finish` node.

## 2. Workflow structure

```text
START
  |
  v
review_node
  |
  +-- status == "approved"
  |       |
  |       v
  |     finish_node
  |       |
  |       v
  |      END
  |
  +-- otherwise
          |
          v
     review_again_node
          |
          v
         END
```

The `review_node` makes the routing decision by returning `Command`.

## 3. Command versus conditional edges

With conditional edges, routing is generally defined separately from the node that updates state.

With `Command`, a node can combine its state update and routing decision in one return value.

Use `Command` when the next destination naturally depends on a decision made inside the node. Use conditional edges when you want routing logic to remain separate.

## 4. Important behavior

`goto` selects the next node, but it does not automatically terminate the graph.

In this lesson, both `finish_node` and `review_again_node` connect to `END`, so either path ends the workflow.

## 5. Run the workflow

```bash
uv run python 00-python-workflows/langgraph_command_workflow.py
```

Try both initial states:

- `"status": "approved"` routes to `finish_node`.
- `"status": "needs_review"` routes to `review_again_node`.

## 6. Run the tests

Test this lesson:

```bash
uv run python -m unittest 00-python-workflows/tests/test_langgraph_command_workflow.py -v
```

Run the complete suite:

```bash
uv run python -m unittest discover -s 00-python-workflows/tests -v
```

The complete suite passed with 45 tests during verification.

## 7. Exercises

1. What are the responsibilities of `update` and `goto`?
2. Why does `Command` make a separate conditional edge unnecessary in this example?
3. What happens if `goto` names a node that does not exist?
4. Why do we explicitly connect the destination nodes to `END`?
5. When might a separate conditional edge be easier to maintain than `Command`?

## Key takeaway

`Command` combines state updates and dynamic routing in a single node return value. It is useful when a node's decision determines both what changes in state and where execution should continue.
