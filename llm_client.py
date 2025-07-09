# llm_client.py
import os
import google.generativeai as genai

# --- IMPORTANT ---
# Do NOT hardcode API keys. Use environment variables for security.
# The API key will be read from the environment variable named 'GEMINI_API_KEY'.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY environment variable not set. Please set it securely.")

# Setup for Gemini
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

def generate_response(prompt):
    """
    Generates a response from the Gemini model.
    """
    try:
        response = gemini_model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=1024,
                top_p=1
            )
        )
        return response.text
    except Exception as e:
        return f"An error occurred with the LLM API: {e}"
