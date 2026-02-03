import requests
from PIL import Image
from io import BytesIO
from config import HF_API_KEY
import time

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

def generate_product_image(product_name, description):
    prompt = (
        f"High quality realistic product photo of {product_name}. "
        f"{description}. Studio lighting, white background, professional."
    )

    payload = {"inputs": prompt}

    # Try twice (handles model cold start)
    for attempt in range(2):
        response = requests.post(API_URL, headers=HEADERS, json=payload)

        # ✅ Success
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))

        # ⏳ Model loading (very common)
        if response.status_code == 503:
            time.sleep(15)  # wait for model to load
            continue

        # ❌ Other errors
        break

    return None
