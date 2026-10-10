# Phase 00 — Python Workflows

## Lesson 01: Sequential Workflow

### Learning objectives

By completing this lesson, you will understand:

- How to organize a workflow into functions.
- How data passes between sequential steps.
- How dictionary unpacking creates an updated dictionary.
- What happens when a workflow step raises an unhandled exception.

### What is a workflow?

A workflow is a sequence of operations organized to accomplish a task. Each operation may consume input, perform work, and produce output for a later operation.

In this lesson, we simulate a small pull-request review workflow:

1. Receive pull-request data.
2. Inspect the changes.
3. Generate a review summary.

The workflow uses plain Python. No LangGraph, LLM, or external service is required.

### Project structure

```text
00-python-workflows/
├── README.md
└── sequential_workflow.py
```

### Implementation

See [`sequential_workflow.py`](./sequential_workflow.py) for the complete runnable implementation.

The program defines three processing functions and a `main()` function that orchestrates them.

#### Step 1: Receive the pull request

`receive_pull_request()` creates a dictionary containing the pull-request number, title, and number of changed files.

In a real application, this data might come from a GitHub API or webhook. Here, we use fixed sample data to keep the lesson focused.

#### Step 2: Inspect changes

`inspect_changes(pr)` receives the dictionary produced by the previous step.

It returns a new dictionary containing the existing fields and an additional `review_status` field.

The dictionary unpacking expression `**pr` inserts the existing key-value pairs into the new dictionary. This is a shallow copy: nested mutable objects are not recursively copied.

Passing the input explicitly also makes the function easier to test independently.

#### Step 3: Generate a summary

`generate_summary(review)` receives the updated dictionary and adds a human-readable summary.

The summary uses values from the input dictionary rather than repeating the pull-request details as hard-coded text.

#### Orchestrate the workflow

`main()` calls the functions in a fixed order:

```python
pr = receive_pull_request()
review = inspect_changes(pr)
result = generate_summary(review)
```

Each function must return successfully before the next assignment can complete.

### Run the lesson

From the repository root, execute:

```bash
python 00-python-workflows/sequential_workflow.py
```

### Expected output

```text
Step 1: Receiving pull request
Step 2: Inspecting changes
Step 3: Generating summary

Final result:
{'pr_number': 42, 'title': 'Fix authentication validation', 'files_changed': 3, 'review_status': 'changes inspected', 'summary': 'PR #42: Fix authentication validation — 3 files changed.'}
```

### Experiment: Simulate a failure

Temporarily replace the body of `inspect_changes()` with:

```python
def inspect_changes(pr: dict) -> dict:
    print("Step 2: Inspecting changes")
    raise RuntimeError("Simulated inspection failure")
```

Run the program again.

The program prints the first two step messages and then displays a traceback. Step 3 and the final result are not reached because the exception is unhandled.

Restore the original implementation after completing the experiment.

### Key concepts

- **Sequential execution:** Steps run in the order specified by the orchestrator.
- **Explicit data flow:** A function receives its input through arguments and returns its result.
- **Transformation:** A processing step can produce an updated representation of its input.
- **Exception propagation:** An unhandled exception interrupts normal execution and propagates up the call stack.
- **Orchestration:** `main()` determines which step runs and when.

### Exercises

1. Change the pull-request number from `42` to `100` and verify that the final summary changes.
2. Add a `branch` field to the initial dictionary and confirm that it survives both transformations.
3. Add a `reviewer` field in `inspect_changes()` without modifying the original input dictionary.
4. Explain why Step 3 doesn't execute when Step 2 raises an unhandled exception.
5. Write a unit test for `generate_summary()` using a dictionary you construct directly.

### Limitations

This example is intentionally simple. It does not include conditional routing, retries, persistent state, asynchronous execution, or external integrations. Those capabilities will be introduced in later lessons.

### Further reading

- [Python tutorial: Defining functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Python tutorial: Dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)
- [Python tutorial: Errors and exceptions](https://docs.python.org/3/tutorial/errors.html)
