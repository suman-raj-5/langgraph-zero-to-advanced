# Lesson 07 — Fan-Out and Fan-In in Python

## Learning objectives

By the end of this lesson, you will understand how to:

- Split a workflow into independent tasks.
- Pass the same input to multiple branches.
- Keep branch results separate.
- Combine results into a final report.
- Handle branches that return empty results.
- Distinguish independent execution from concurrent execution.

## 1. What is fan-out?

Fan-out means distributing work across multiple branches.

In this lesson, a pull request is reviewed by two independent functions:

- `security_review()` checks for security concerns.
- `test_review()` identifies testing gaps.

Both functions receive the same pull request input and return their own results.

## 2. What is fan-in?

Fan-in means combining the results of multiple branches into a single output.

The `combine_reviews()` function:

1. Preserves the original pull request details.
2. Stores each branch result separately.
3. Combines their findings lists.
4. Calculates the total number of findings.

## 3. Workflow structure

The workflow follows this sequence:

1. `receive_pull_request()` creates the input.
2. `security_review()` produces security findings.
3. `test_review()` produces testing findings.
4. `combine_reviews()` merges the results.
5. The final report contains the original PR details and all review findings.

## 4. Handling empty results

One experiment changed the security branch to return an empty findings list.

The test branch still returned one finding, and the combined report correctly contained one finding.

This works because concatenating an empty list with a non-empty list preserves the non-empty list.

An empty result is not necessarily an error. The workflow should distinguish a valid empty result from a branch that failed to execute.

## 5. Important implementation detail

This lesson executes both branches sequentially:

```python
security_result = security_review(pr)
test_result = test_review(pr)
```

Although the branches have independent inputs and outputs, this code does not run them concurrently.

True parallel execution requires concurrency mechanisms such as threads, processes, or asynchronous tasks, depending on the workload.

## 6. Run the lesson

From the repository root:

```bash
python 00-python-workflows/fan_out_workflow.py
```

Expected behavior:

- Both branches execute.
- The security branch returns one finding.
- The test branch returns one finding.
- The combined report contains two findings.

No external API or additional dependency is required.

## 7. Experiments performed

### Experiment A — Both branches return findings

The combined report contains two findings.

### Experiment B — Security branch returns no findings

The combined report contains only the test branch's finding. The workflow completes without an exception.

After the experiment, restore the original security finding and verify the standard scenario again.

## 8. Exercises

1. Add a third branch called `performance_review()`.
2. Give it one finding and include its result in the combined report.
3. Update `total_findings` so it includes findings from all three branches.
4. What should happen if all branches return empty findings lists?
5. How would the design need to change if one branch raises an exception?
6. Why does sequential fan-out differ from concurrent fan-out?

## 9. Connection to LangGraph

LangGraph can represent branching and parallel work as graph execution. Its `Send` mechanism supports dynamically creating tasks, while downstream nodes can combine results.

This lesson builds the conceptual foundation for fan-out/fan-in and map-reduce workflows. Our implementation is plain Python and executes the branches sequentially.

## 10. References

- [Python documentation — Data structures](https://docs.python.org/3/tutorial/datastructures.html)
- [Python documentation — Concurrent execution](https://docs.python.org/3/library/concurrent.futures.html)
- [LangGraph — Official documentation](https://docs.langchain.com/oss/python/langgraph/overview)
