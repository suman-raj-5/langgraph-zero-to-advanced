# Lesson 09 — Workflow Composition and Reusable Steps

## 1. Objective

Learn how to compose a workflow from small, reusable Python functions. Each function performs one responsibility, accepts input, and returns output.

This prepares us for representing workflow steps as LangGraph nodes later.

## 2. What is workflow composition?

Workflow composition means connecting smaller functions so that the output of one step becomes the input to another.

Our example follows this sequence:

1. `receive_pull_request()` creates the initial pull request state.
2. `validate_pull_request(pr)` checks required fields and adds a validation status.
3. `create_summary(pr)` creates a compact summary from the validated state.

## 3. Project structure

```text
00-python-workflows/
├── composed_workflow.py
├── fan_out_workflow.py
├── tests/
│   ├── test_composed_workflow.py
│   └── test_fan_out_workflow.py
└── lesson-09-workflow-composition.md
```

## 4. Reusable functions

Each function has one clear responsibility:

- **Receive:** creates the initial data.
- **Validate:** checks the required fields and returns validated state.
- **Summarize:** extracts the information needed for a report.

This separation makes functions easier to reuse, test, and maintain.

## 5. State transformation

The validation function returns:

```python
return {
    **pr,
    "status": "validated",
}
```

The dictionary unpacking expression `**pr` copies the existing key-value pairs into a new dictionary. The new `status` field is then added.

This leaves the original dictionary unchanged at the top level.

**Important:** this is a shallow copy. Nested mutable objects, such as the `files_changed` list, are still shared between the dictionaries unless explicitly copied.

## 6. Validation and error handling

The workflow rejects invalid inputs by raising `ValueError`.

Examples include:
- Missing or empty pull request title.
- Missing pull request number.
- Empty list of changed files.

A caller can catch an expected exception with `try/except`. Catching the exception handles the error; it does not make the invalid input valid.

## 7. Automated testing

Run all workflow tests from the repository root:

```bash
python -m unittest discover -s 00-python-workflows/tests -v
```

The current suite contains nine tests covering:
- Initial pull request state.
- Review aggregation and empty findings.
- Individual security and test-review functions.
- Validation and state preservation.
- Missing title and empty changed-file list.
- Summary generation.

Expected result:

```text
Ran 9 tests
OK
```

The exact runtime and printed messages may vary.

## 8. Python import paths

The tests currently add the `00-python-workflows` directory to `sys.path` so Python can import the workflow modules during test discovery.

This is a practical learning-stage workaround. A proper Python package structure is preferable as the project grows.

## 9. Exercises

1. Add a validation test for a missing pull request number.
2. Add a test that confirms the original state has no `status` field after validation.
3. Change the workflow to return a different status and update the relevant tests.
4. Try composing an additional function between validation and summary generation.

## 10. Key takeaways

- Compose workflows from small functions with clear responsibilities.
- Pass state explicitly between steps.
- Validate inputs before using them.
- Return transformed state rather than unnecessarily mutating inputs.
- Use automated tests to verify successful and failing paths.

These patterns help prepare for LangGraph, where functions will become nodes and graph edges will control how execution moves between them.

## 11. Reference

- [Python documentation — Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
