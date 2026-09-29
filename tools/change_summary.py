def generate_change_summary(
    bug_report,
    root_cause_analysis,
    generated_fix,
    file_path,
    targeted_passed,
    regression_passed
):
    """
    Generate a concise change summary for the validated fix.
    """

    status = (
        "Validated and approved"
        if targeted_passed and regression_passed
        else "Validation failed"
    )

    summary = f"""
BUG FIX SUMMARY
===============

Bug Report:
{bug_report}

Root Cause:
{root_cause_analysis}

File Changed:
{file_path}

Generated Fix:
{generated_fix}

Validation:
- Targeted Bug Test: {"PASS" if targeted_passed else "FAIL"}
- Regression Tests: {"PASS" if regression_passed else "FAIL"}

Status:
{status}
"""

    return summary.strip()