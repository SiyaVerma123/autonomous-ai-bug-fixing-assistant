from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Explain in one sentence what a ZeroDivisionError means in Python."
)

print("Gemini response:")
print(response.text)