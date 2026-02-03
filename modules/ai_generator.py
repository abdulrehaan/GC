import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure API
genai.configure(api_key=GEMINI_API_KEY)

# Gemini 2.5 Flash model
model = genai.GenerativeModel("models/gemini-2.5-flash")

def generate_content(prompt: str) -> str:
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 300
        }
    )
    return response.text
