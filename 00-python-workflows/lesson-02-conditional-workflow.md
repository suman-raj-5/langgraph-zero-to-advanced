# Lesson 02: Conditional Workflows in Plain Python

## Learning objectives

By completing this lesson, you will understand:

- How a workflow makes a routing decision.
- How `if/else` selects a path.
- How `any()` evaluates a collection of conditions.
- Why decision-making and execution should be separate responsibilities.

## What is a conditional workflow?

A sequential workflow follows a fixed order. A conditional workflow chooses between possible paths based on data or a condition.

In this lesson, we simulate a pull-request review workflow:

- Pull requests touching filenames containing `auth` take the security-review path.
- Other pull requests take the standard-review path.

This is a simplified teaching rule, not a production security classifier.

## Project structure

```text
00-python-workflows/
├── README.md
├── sequential_workflow.py
├── conditional_workflow.py
└── lesson-02-conditional-workflow.md
```

## Run the example

From the repository root, execute:

```bash
python 00-python-workflows/conditional_workflow.py
```

The current example uses a product-catalog pull request and selects the standard-review path.

## How routing works

The routing function contains the decision logic:

```python
def route_review(pr: dict) -> str:
    if any("auth" in filename.lower() for filename in pr["files_changed"]):
        return "security_review"

    return "standard_review"
```

### Understanding the condition

- `pr["files_changed"]` returns the list of changed filenames.
- `filename.lower()` makes the comparison case-insensitive.
- `"auth" in filename.lower()` checks for the substring `auth`.
- `any(...)` returns `True` if at least one filename matches.

The function returns a route identifier rather than executing either review itself.

## Decision versus execution

The orchestrator uses the returned route:

```python
route = route_review(pr)
print(f"Selected route: {route}")

if route == "security_review":
    result = security_review(pr)
else:
    result = standard_review(pr)
```

The responsibilities are deliberately separated:

- `route_review()` decides.
- `main()` orchestrates.
- The selected review function executes.

This separation makes routing logic easier to test and maintain.

## Experiments

### Experiment 1: Security-review route

Use these changed files:

```python
["src/authentication.py", "tests/test_authentication.py"]
```

Expected route:

```text
Selected route: security_review
```

### Experiment 2: Standard-review route

Use these changed files:

```python
["src/catalog.py", "tests/test_catalog.py"]
```

Expected route:

```text
Selected route: standard_review
```

### Experiment 3: Empty file list

Try:

```python
"files_changed": []
```

Because there are no filenames matching the condition, the current implementation selects `standard_review`.

## Exercises

1. Change the filename to `src/AUTH_service.py`. Does the security-review route still get selected?
2. Add `src/authentication_helpers.py` to an otherwise standard pull request. What happens?
3. Replace `any()` with an explicit loop. Does the routing behavior remain the same?
4. Add a third route for documentation-only changes.
5. Explain why the routing function returns a string instead of calling the review functions directly.

## Limitations

Filename substring matching is only an educational rule. A production review system should use explicit policies and reliable change metadata rather than assume that a filename alone determines security risk.

## Key takeaways

- Conditional workflows select paths based on data.
- Routing decisions can be separated from execution.
- `any()` is useful when a condition should match at least one element.
- Testing multiple branches is essential for validating routing logic.

## Further reading

- [Python control flow](https://docs.python.org/3/tutorial/controlflow.html)
- [Python built-in functions: `any()`](https://docs.python.org/3/library/functions.html#any)
