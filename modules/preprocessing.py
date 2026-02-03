import re

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9,.\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def preprocess_inputs(product, description, audience, keywords):
    return {
        "product": clean_text(product),
        "description": clean_text(description),
        "audience": clean_text(audience),
        "keywords": clean_text(keywords)
    }
