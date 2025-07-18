import os
from google import genai

# --- IMPORTANT ---
# Do NOT hardcode API keys. Use environment variables for security.
# The API key will be read from the environment variable named 'GEMINI_API_KEY'.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY environment variable not set. Please set it securely.")

# Setup for Google Gemini
# The client automatically gets the API key from the environment variable
client = genai.Client(api_key=GEMINI_API_KEY)

def generate_response(prompt):
    """
    Generates a response from the Google Gemini model.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",  # Using Gemini 2.5 Flash, can be changed to other versions like gemini-2.5-pro
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"An error occurred with the LLM API: {e}"
