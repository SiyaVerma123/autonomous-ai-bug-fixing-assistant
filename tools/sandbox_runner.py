import os
import shutil
import subprocess
import sys
from datetime import datetime


def run_pytest(sandbox_root, test_filter=None):
    """Run pytest inside the sandbox."""

    command = [sys.executable, "-m", "pytest"]

    if test_filter:
        command.extend(["-k", test_filter])

    result = subprocess.run(
        command,
        cwd=sandbox_root,
        capture_output=True,
        text=True
    )

    return result


def run_tests_in_sandbox(repo_path, fixed_file_path, fixed_code):
    """
    Create an isolated copy of the repository, apply the generated fix,
    and run targeted and regression tests.
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    sandbox_root = os.path.join(
        "outputs",
        f"sandbox_run_{timestamp}"
    )

    os.makedirs("outputs", exist_ok=True)

    # Create isolated repository copy.
    shutil.copytree(repo_path, sandbox_root)

    # Apply generated fix only inside sandbox.
    target_file = os.path.join(
        sandbox_root,
        fixed_file_path
    )

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(fixed_code)

    # Targeted bug test
    targeted_result = run_pytest(
        sandbox_root,
        "test_divide_by_zero"
    )

    # Regression tests
    regression_result = run_pytest(
        sandbox_root,
        "not test_divide_by_zero"
    )

    targeted_passed = targeted_result.returncode == 0
    regression_passed = regression_result.returncode == 0

    return {
        "sandbox_path": sandbox_root,

        "targeted_passed": targeted_passed,
        "targeted_return_code": targeted_result.returncode,
        "targeted_output": targeted_result.stdout,
        "targeted_error": targeted_result.stderr,

        "regression_passed": regression_passed,
        "regression_return_code": regression_result.returncode,
        "regression_output": regression_result.stdout,
        "regression_error": regression_result.stderr,

        "passed": targeted_passed and regression_passed,
    }


if __name__ == "__main__":

    repo_path = "demo_repo"

    fixed_file_path = os.path.join(
        "app",
        "calculator.py"
    )

    fixed_code = """def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def divide(a, b):
    if b == 0:
        return None
    return a / b
"""

    result = run_tests_in_sandbox(
        repo_path,
        fixed_file_path,
        fixed_code
    )

    print("=== SANDBOX VALIDATION ===")

    print(f"Sandbox: {result['sandbox_path']}")

    print("\n--- TARGETED BUG TEST ---")
    print(f"Passed: {result['targeted_passed']}")
    print(result["targeted_output"])

    if result["targeted_error"]:
        print(result["targeted_error"])

    print("\n--- REGRESSION TESTS ---")
    print(f"Passed: {result['regression_passed']}")
    print(result["regression_output"])

    if result["regression_error"]:
        print(result["regression_error"])

    print("\n--- OVERALL RESULT ---")
    print(f"All validation passed: {result['passed']}")