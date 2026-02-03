from groq import Groq
<<<<<<< HEAD
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
=======
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)
>>>>>>> 259735af47a4dd1ddfd0685fe05e84ceec63cc34

def generate_content(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
<<<<<<< HEAD
            model="llama-3.1-8b-instant",
=======
            model="llama-3.3-70b-versatile",  # Best balance: strong copywriting + fast
            # Alternatives: "llama-3.1-8b-instant" (cheaper & faster), "gemma2-9b-it" (good creative)
>>>>>>> 259735af47a4dd1ddfd0685fe05e84ceec63cc34
            messages=[{"role": "user", "content": prompt}],
            temperature=0.75,
            max_tokens=1536,
            top_p=0.92,
            stream=False
        )
<<<<<<< HEAD

        text = response.choices[0].message.content.strip()
        print(f"DEBUG: Generated {len(text.split())} words")
        return text

    except Exception as e:
        return f"Groq API error: {str(e)} – check key/quota or try again."
=======
        text = response.choices[0].message.content.strip()
        print(f"DEBUG: Generated {len(text.split())} words")
        return text
    except Exception as e:
        return f"Groq API error: {str(e)} – check key/quota or try again."
>>>>>>> 259735af47a4dd1ddfd0685fe05e84ceec63cc34
