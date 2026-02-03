import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env
load_dotenv()

# Initialize Groq client securely using env variable
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_content(prompt: str) -> str:
    """
    Generate marketing content using Groq LLM.
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Best balance: quality + speed
            messages=[
                {"role": "system", "content": "You are a professional marketing copywriter."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.75,
            max_tokens=1536,
            top_p=0.92,
            stream=False
        )

        text = response.choices[0].message.content.strip()
        print(f"DEBUG: Generated {len(text.split())} words")
        return text

    except Exception as e:
        return f"Groq API error: {str(e)} – check key/quota or try again."
