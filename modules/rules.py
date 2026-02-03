def apply_rules(text, tone):
    if tone == "Professional":
        return text.replace("!", ".")
    elif tone == "Persuasive":
        return text + "\n\n👉 Start your journey today."
    elif tone == "Friendly":
        return "😊 " + text
    return text
