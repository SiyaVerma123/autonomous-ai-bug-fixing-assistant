from google import genai
def analyze_bug(bug_report, source_code, test_output):
    client = genai.Client()
    prompt = f"""
You are a software debugging analyst.
Analyze the following bug report, source code, and test output.
BUG REPORT:
{bug_report}
SOURCE CODE:
{source_code}
TEST OUTPUT:
{test_output}
Provide a concise root-cause analysis.
Your response must contain:
1. Bug Summary
2. Root Cause
3. Faulty Code Location
4. Expected Behavior
5. Suggested Fix
Do not modify the code.
Do not invent information that is not present in the inputs.
"""
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    bug_report = """
The divide function crashes when the second argument is zero.
Error:
ZeroDivisionError: division by zero
Expected Behavior:
When the denominator is zero, the function should return None
instead of crashing.
"""
    source_code = """
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def divide(a, b):
    return a / b
"""
    test_output = """
FAILED tests/test_calculator.py::test_divide_by_zero
ZeroDivisionError: division by zero
"""
    result = analyze_bug(
        bug_report,
        source_code,
        test_output
    )
    print("=== ROOT CAUSE ANALYSIS ===")
    print(result)