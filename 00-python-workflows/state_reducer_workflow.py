
def security_review() -> list[str]:
    """Return findings from the security review."""
    return ["SQL injection risk"]


def test_review() -> list[str]:
    """Return findings from the test review."""
    return ["Missing test coverage"]


def merge_findings(
    existing: list[str],
    incoming: list[str],
) -> list[str]:
    """Combine existing findings with incoming findings."""
    return existing + incoming


def main() -> None:
    security_findings = security_review()
    test_findings = test_review()

    findings = security_findings
    findings = merge_findings(findings, test_findings)

    print("Security findings:", security_findings)
    print("Test findings:", test_findings)
    print("Combined findings:", findings)
    print("\nAdditional merge tests:")
    print("Empty incoming:", merge_findings(["Existing finding"], []))
    print("Empty existing:", merge_findings([], ["New finding"]))
    print(
        "Multiple findings:",
        merge_findings(
            ["Security issue", "Authentication issue"],
            ["Missing test"],
        ),
    )


if __name__ == "__main__":
    main()
