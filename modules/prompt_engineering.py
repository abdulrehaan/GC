def create_prompt(data, tone, content_type):
    if content_type == "Promotional Email":
        return f"""
You are a professional email marketing specialist.

Write a COMPLETE and ENGAGING promotional email.

Product Name: {data['product']}
Description: {data['description']}
Target Audience: {data['audience']}
SEO Keywords: {data['keywords']}

MANDATORY EMAIL STRUCTURE:
- Subject line
- Greeting
- Opening paragraph (problem + curiosity)
- Product introduction
- Key features (in bullet points)
- Benefits for the reader
- Strong call to action
- Friendly closing and signature

WRITING RULES:
- Tone: {tone}
- Minimum length: 200–250 words
- Use short paragraphs for readability
- Make the email visually engaging and persuasive
- Do NOT stop after the introduction
"""
    else:
        return f"""
You are a professional marketing copywriter.

Generate a detailed and engaging {content_type}.

Product Name: {data['product']}
Description: {data['description']}
Target Audience: {data['audience']}
SEO Keywords: {data['keywords']}

WRITING RULES:
- Tone: {tone}
- Write multiple paragraphs
- Clearly explain features and benefits
- End with a strong call to action
"""
