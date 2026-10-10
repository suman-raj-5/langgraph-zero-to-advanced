# Lesson 03: Loops and Repeated Workflow Execution

## Learning objectives

By completing this lesson, you will understand:

- How a `while` loop repeats workflow steps.
- How updated state is carried between iterations.
- How completion conditions control termination.
- Why a maximum-iteration limit is a useful safeguard.

## What is a looping workflow?

A sequential workflow executes steps in a fixed sequence. A looping workflow repeats a step while a condition remains true.

In this lesson, we simulate a review process that improves a quality score on each attempt. The loop stops when the target score is reached or the maximum number of attempts is exhausted.

The score progression is simulated for learning purposes; it does not represent a real code-quality measurement.

## Project structure

```text
00-python-workflows/
├── README.md
├── sequential_workflow.py
├── conditional_workflow.py
├── loop_workflow.py
├── lesson-02-conditional-workflow.md
└── lesson-03-loops.md
```

## Run the example

From the repository root:

```bash
python 00-python-workflows/loop_workflow.py
```

With the default configuration, the workflow completes in three attempts.

## Understanding the state

The initial state contains:

- `attempt`: number of iterations completed.
- `quality_score`: current simulated score.
- `target_score`: score required for completion.
- `max_attempts`: maximum number of permitted iterations.

The loop uses this condition:

```python
while (
    state["quality_score"] < state["target_score"]
    and state["attempt"] < state["max_attempts"]
):
    state = review_iteration(state)
```

Both conditions must be true for another iteration to run.

### Carrying state between iterations

The assignment `state = review_iteration(state)` replaces the current state variable with the updated dictionary returned by the function.

The next loop-condition check therefore evaluates the updated attempt count and quality score.

### Termination conditions

The workflow has two ways to stop:

1. The quality score reaches the target.
2. The maximum number of attempts is reached.

After the loop, the program checks whether the target was reached and sets the final status accordingly.

## Experiments

### Experiment 1: Successful completion

Use:

```python
"target_score": 3,
"max_attempts": 5,
```

Expected result: three attempts and `"status": "completed"`.

### Experiment 2: Maximum attempts reached

Use:

```python
"target_score": 10,
"max_attempts": 3,
```

Expected result: three attempts and `"status": "maximum attempts reached"`.

Restore the original configuration after the experiment.

## Exercises

1. Change the target score to `2`. How many iterations execute?
2. Set `max_attempts` to `1`. What happens when the target is `3`?
3. Explain why the loop condition uses `and` rather than `or`.
4. What could happen if the loop had no effective termination condition?
5. Modify `review_iteration()` so that the score increases by two per attempt, without exceeding the target.

## Key takeaways

- Loops repeat work while a condition remains true.
- Workflow state can be updated and carried across iterations.
- Completion conditions define when the work is finished.
- Maximum-iteration limits protect against unbounded execution.

## Limitations

This is a synchronous, in-memory example. It does not implement retries for exceptions, persistent state, asynchronous tasks, or recovery after process failure. Those concepts will be explored in later lessons.

## Further reading

- [Python control flow: `while` statements](https://docs.python.org/3/tutorial/controlflow.html#while-statements)
- [Python built-in functions](https://docs.python.org/3/library/functions.html)
