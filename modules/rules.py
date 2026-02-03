def apply_rules(text, tone):
    if tone == "Professional":
        return text.replace("!", ".").replace("!!", ".")
    elif tone == "Persuasive":
        # Add only at the very end if not already present
        if "Start your journey today" not in text:
            return text.strip() + "\n\n👉 **Start your journey today – limited stock!**"
        return text
    elif tone == "Friendly":
        return "😊 " + text.strip()
    return text