def create_prompt(data, tone, content_type):
    # Few-shot example for Social Media Post (to guide "awestruck" style)
    example_social = """
   **Tired of gym commutes killing your motivation?** 😩🚗

   Imagine crushing full-body workouts from your couch – anytime!  

   Meet our **Resistance Band Set** – your portable power gym! 💪  

   🔥 **Why it's a game-changer:**
   - 5 bands up to **1040kg resistance** for progressive gains
   - Non-slip handles + comfy ankle straps = zero hassle
   - Door anchor for 50+ exercises anywhere
   - Bonus carry bag & PDF guide to get started FAST  

   Busy pros & home warriors: Ditch memberships, build strength on your terms. Results in weeks!  

   **Grab yours now – limited stock!** 👉 [Link]  

   #HomeWorkout #ResistanceBands #FitnessHack #NoGymNeeded #StrengthTraining
   """

    base_rules = f"""
   WRITING RULES:
   - Tone: {tone} – make it exciting, relatable, and urgent.
   - Start with a **bold hook** (question or pain point, 1 line max).
   - Short paragraphs (2–4 lines) + 3–6 emojis for visual pop.
   - **Bold** product name & key phrases.
   - Bullet features/benefits: 4–6 punchy lines with action words.
   - Build desire: 1–2 sentences on transformation/social proof.
   - End with **urgent CTA** (e.g. "Grab now – limited!").
   - For Social Media: 120–220 words + 5–8 targeted hashtags.
   - Output plain markdown only – no HTML, no extras.
   - Make it scroll-stopping: persuasive, benefit-first, fun!

   EXAMPLE FOR SOCIAL POST (follow this style exactly):
   {example_social}
   """

    if content_type == "Promotional Email":
        return f"""
   You are a conversion-obsessed email copywriter.

   Write a full promotional email.

   Product: {data['product']}
   Description: {data['description']}
   Audience: {data['audience']}
   Keywords: {data['keywords']}

   STRUCTURE:
   - Subject: [Catchy + urgent]
   - Greeting
   - Hook para
   - Product intro
   - Features bullets
   - Benefits para
   - CTA para
   - Sign-off

   {base_rules}
   - 250–350 words, mobile-friendly.
   """

    elif content_type == "Social Media Post":
        return f"""
   You are a viral social media copywriter (Instagram/FB expert).

   Create one killer post.

   Product: {data['product']}
   Description: {data['description']}
   Audience: {data['audience']}
   Keywords: {data['keywords']}

   {base_rules}
   - Match the example's energy: hook → excitement → bullets → desire → CTA → hashtags.
   - Use keywords naturally for SEO.
   """

    else:
        return f"""
   You are a pro copywriter.

   Generate engaging {content_type}.

   Product: {data['product']}
   Description: {data['description']}
   Audience: {data['audience']}
   Keywords: {data['keywords']}

   {base_rules}
   - Clear structure, benefit-focused.
   """
