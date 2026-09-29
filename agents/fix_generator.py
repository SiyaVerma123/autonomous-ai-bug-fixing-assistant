from google import genai
def generate_fix(source_code, root_cause_analysis):
    client = genai.Client()
    prompt = f"""
You are a software engineer responsible for generating a minimal code fix.
SOURCE CODE:
{source_code}
ROOT CAUSE ANALYSIS:
{root_cause_analysis}
Generate the corrected version of the source code.
Rules:
1. Fix only the identified bug.
2. Preserve all existing functionality.
3. Make the smallest reasonable change.
4. Do not add unnecessary features.
5. Return ONLY the complete corrected Python source code.
6. Do not include Markdown code fences.
7. Do not include explanations.
"""
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )
    return response.text.strip()
if __name__ == "__main__":
    source_code = """def add(a, b):
    return a + b
def subtract(a, b):
    return a - b
def divide(a, b):
    return a / b
"""
    root_cause_analysis = """
1. Bug Summary:
The divide function crashes with a ZeroDivisionError when attempting
to divide a number by zero.
2. Root Cause:
The divide function performs a / b without checking whether b is zero.
3. Faulty Code Location:
Function divide(a, b).
4. Expected Behavior:
When b is zero, the function should return None.
5. Suggested Fix:
Add a conditional check inside divide() to return None if b == 0.
"""
    fixed_code = generate_fix(
        source_code,
        root_cause_analysis
    )
    print("=== GENERATED FIX ===")
    print(fixed_code)