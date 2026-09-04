import os
from dotenv import load_dotenv
from google import genai

# Load GEMINI_API_KEY from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("WARNING: GEMINI_API_KEY is not set in D:\\gitM\\01_ContentFactory\\.env")
    print("Please open D:\\gitM\\01_ContentFactory\\.env and paste your API key from https://aistudio.google.com/")
else:
    try:
        client = genai.Client(api_key=api_key)
        # Test Gemini 2.5/3.0/Flash model
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Give me one sentence describing a cinematic underground data center."
        )
        print("\n=== GEMINI API TEST SUCCESSFUL ===")
        print(f"Model Response: {response.text.strip()}")
        print("==================================\n")
    except Exception as e:
        print(f"Error testing Gemini API: {e}")
