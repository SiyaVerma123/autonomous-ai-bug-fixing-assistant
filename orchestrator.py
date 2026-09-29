import os
import subprocess
import sys

from agents.bug_analyzer import analyze_bug
from agents.fix_generator import generate_fix
from tools.sandbox_runner import run_tests_in_sandbox
from tools.apply_fix import apply_fix
from tools.change_summary import generate_change_summary


REPO_PATH = "demo_repo"
BUG_REPORT_PATH = "bug_report.txt"
SOURCE_FILE = os.path.join("app", "calculator.py")

MAX_ATTEMPTS = 2


def run_initial_tests():
    result = subprocess.run(
        [sys.executable, "-m", "pytest"],
        cwd=REPO_PATH,
        capture_output=True,
        text=True
    )

    return result


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():

    print("=" * 60)
    print("AUTONOMOUS AI BUG FIXING ASSISTANT")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. Load bug report and source code
    # ---------------------------------------------------------

    print("\n[1] Loading bug report and source code...")

    bug_report = read_file(BUG_REPORT_PATH)

    source_path = os.path.join(
        REPO_PATH,
        SOURCE_FILE
    )

    source_code = read_file(source_path)

    # ---------------------------------------------------------
    # 2. Run initial tests
    # ---------------------------------------------------------

    print("\n[2] Running initial tests...")

    initial_test_result = run_initial_tests()

    test_output = (
        initial_test_result.stdout
        + "\n"
        + initial_test_result.stderr
    )

    print(test_output)

    if initial_test_result.returncode == 0:
        print("No failing tests detected.")
        return

    print("Initial tests failed. Proceeding with AI analysis.")

    # ---------------------------------------------------------
    # 3. Bug Analyst Agent
    # ---------------------------------------------------------

    print("\n[3] Running Bug Analyst Agent...")

    root_cause_analysis = analyze_bug(
        bug_report,
        source_code,
        test_output
    )

    print("\n=== ROOT CAUSE ANALYSIS ===")
    print(root_cause_analysis)

    # ---------------------------------------------------------
    # 4. Fix generation + validation loop
    # ---------------------------------------------------------

    current_source_code = source_code

    for attempt in range(1, MAX_ATTEMPTS + 1):

        print("\n" + "=" * 60)
        print(f"FIX ATTEMPT {attempt} OF {MAX_ATTEMPTS}")
        print("=" * 60)

        # -----------------------------------------------------
        # Generate fix
        # -----------------------------------------------------

        print("\n[4] Running Fix Generator Agent...")

        generated_fix = generate_fix(
            current_source_code,
            root_cause_analysis
        )

        print("\n=== GENERATED FIX ===")
        print(generated_fix)

        # -----------------------------------------------------
        # Sandbox validation
        # -----------------------------------------------------

        print(
            "\n[5] Testing generated fix in isolated sandbox..."
        )

        sandbox_result = run_tests_in_sandbox(
            REPO_PATH,
            SOURCE_FILE,
            generated_fix
        )

        print("\n=== SANDBOX VALIDATION ===")

        print(
            f"Sandbox: {sandbox_result['sandbox_path']}"
        )

        print("\n--- TARGETED BUG TEST ---")

        print(
            f"Passed: {sandbox_result['targeted_passed']}"
        )

        print(
            sandbox_result["targeted_output"]
        )

        if sandbox_result["targeted_error"]:
            print(
                sandbox_result["targeted_error"]
            )

        print("\n--- REGRESSION TESTS ---")

        print(
            f"Passed: {sandbox_result['regression_passed']}"
        )

        print(
            sandbox_result["regression_output"]
        )

        if sandbox_result["regression_error"]:
            print(
                sandbox_result["regression_error"]
            )

        # -----------------------------------------------------
        # Successful validation
        # -----------------------------------------------------

        if sandbox_result["passed"]:

            print("\n" + "=" * 60)
            print("FIX VALIDATED SUCCESSFULLY")
            print("=" * 60)

            print(
                f"\nSuccessful validation on attempt {attempt}."
            )

            print(
                "The AI-generated fix passed both "
                "targeted and regression tests."
            )

            print(
                "The original repository has not been modified yet."
            )

            print(
                f"Validated copy: "
                f"{sandbox_result['sandbox_path']}"
            )

            # -------------------------------------------------
            # Approval gate
            # -------------------------------------------------

            print("\n=== APPROVAL REQUIRED ===")

            approval = input(
                "\nApply this validated fix to the "
                "original repository? (yes/no): "
            ).strip().lower()

            if approval == "yes":

                # -------------------------------------------------
                # Apply validated fix
                # -------------------------------------------------

                applied_file = apply_fix(
                    REPO_PATH,
                    SOURCE_FILE,
                    generated_fix
                )

                print("\nFix approved and applied.")

                print(
                    f"Updated file: {applied_file}"
                )

                # -------------------------------------------------
                # Generate change summary
                # -------------------------------------------------

                change_summary = generate_change_summary(
                    bug_report,
                    root_cause_analysis,
                    generated_fix,
                    applied_file,
                    sandbox_result["targeted_passed"],
                    sandbox_result["regression_passed"]
                )

                print("\n" + "=" * 60)
                print("CODE CHANGE / PR SUMMARY")
                print("=" * 60)

                print(change_summary)

                # -------------------------------------------------
                # Save change summary
                # -------------------------------------------------

                os.makedirs("outputs", exist_ok=True)

                summary_path = os.path.join(
                    "outputs",
                    "change_summary.txt"
                )

                with open(
                    summary_path,
                    "w",
                    encoding="utf-8"
                ) as f:
                    f.write(change_summary)

                print(
                    f"\nChange summary saved to: {summary_path}"
                )

            else:

                print("\nFix was not applied.")

                print(
                    "The original repository remains unchanged."
                )

            return

        # -----------------------------------------------------
        # Failed validation
        # -----------------------------------------------------

        print("\n" + "=" * 60)
        print("FIX VALIDATION FAILED")
        print("=" * 60)

        if attempt < MAX_ATTEMPTS:

            print(
                "\nSending validation failure feedback "
                "back to the Fix Generator..."
            )

            root_cause_analysis = (
                root_cause_analysis
                + "\n\nVALIDATION FAILURE FEEDBACK:\n"
                + sandbox_result["targeted_output"]
                + "\n"
                + sandbox_result["targeted_error"]
                + "\n"
                + sandbox_result["regression_output"]
                + "\n"
                + sandbox_result["regression_error"]
            )

            current_source_code = generated_fix

        else:

            print(
                "\nMaximum fix attempts reached."
            )

            print(
                "The assistant could not validate "
                "a successful fix."
            )


if __name__ == "__main__":
    main()