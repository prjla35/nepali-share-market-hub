# llm_client.py
import os
from groq import Groq

# --- IMPORTANT ---
# Do NOT hardcode API keys. Use environment variables for security.
# The API key will be read from the environment variable named 'GROQ_API_KEY'.
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY is None:
    raise ValueError("GROQ_API_KEY environment variable not set. Please set it securely.")

# Setup for Groq
groq_client = Groq(
    api_key=GROQ_API_KEY,
)

def generate_response(prompt):
    """
    Generates a response from the Groq LLaMA model.
    """
    try:
        completion = groq_client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct", # Ensure this model is correct and available
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_completion_tokens=1024,
            top_p=1
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred with the LLM API: {e}"
