# Lesson 08 — Workflow Validation and Testing

## 1. Objective

Learn how to test a Python workflow using the built-in `unittest` framework, without installing additional dependencies.

We use the fan-out/fan-in workflow from Lesson 07 as our example.

## 2. What is testing?

Testing checks whether a function behaves as expected for given inputs.

For example, if a workflow combines security and test findings, we should verify that:
- Both sets of findings appear in the final report.
- The total finding count is correct.
- Empty findings are handled correctly.
- Individual workflow steps return the expected results.

## 3. Project structure

```text
00-python-workflows/
├── fan_out_workflow.py
├── tests/
│   └── test_fan_out_workflow.py
└── lesson-08-testing.md
```

## 4. The `unittest` framework

Python includes `unittest`, so no extra package installation is required.

Important concepts:

- `unittest.TestCase`: a class that groups related tests.
- `test_...()`: a method whose name starts with `test_` and which unittest discovers.
- `assertEqual(a, b)`: verifies that two values are equal.
- `assertIn(item, collection)`: verifies that an item exists in a collection.
- `unittest.main()`: enables running the test module directly.

## 5. What we tested

| Test | Purpose |
|---|---|
| `test_receive_pull_request_returns_expected_state` | Checks the initial pull request state. |
| `test_combine_reviews_merges_findings` | Checks that findings from both branches are combined. |
| `test_combine_reviews_handles_empty_findings` | Checks aggregation when one branch returns no findings. |
| `test_security_review_returns_security_findings` | Checks the security-review function. |
| `test_test_review_returns_test_findings` | Checks the test-review function. |

We also verify that `total_findings` matches `len(all_findings)`.

## 6. Run the tests

Run this command from the `00-python-workflows` directory:

```bash
python -m unittest tests.test_fan_out_workflow -v
```

Expected result:

```text
Ran 5 tests
OK
```

The exact execution time and printed messages may vary.

## 7. What we learned

1. Tests validate expected behavior.
2. Individual functions can be tested independently.
3. Edge cases deserve explicit tests.
4. A failed assertion does not automatically mean the implementation is wrong; the test expectation may also be incorrect.
5. Testing the relationship between output fields can catch inconsistencies.

## 8. Exercises

1. Add a test for an empty list of findings from both branches.
2. Add a test that verifies the report contains both review results.
3. Intentionally change an expected value and observe the failure message.
4. Restore the correct assertion and run the complete test suite again.

## 9. Key takeaway

A workflow may work for one example and still fail for other inputs. Automated tests let us check normal behavior, edge cases, and output consistency before building more complex systems.

This testing foundation will be useful when we later introduce LangGraph nodes, conditional edges, parallel branches, and persistent workflows.

## 10. References

- [Python `unittest` documentation](https://docs.python.org/3/library/unittest.html)
