import streamlit as st
from modules.preprocessing import preprocess_inputs
from modules.prompt_engineering import create_prompt
from modules.ai_generator import generate_content
from modules.rules import apply_rules

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="GenCopy",
    page_icon="🧠",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #020617;
}

.main-title {
    text-align: center;
    font-size: 36px;
    font-weight: 700;
    color: #38bdf8;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 30px;
}

.output-box {
    background-color: #0f172a;
    padding: 24px;
    border-radius: 14px;
    color: #e5e7eb;
    font-size: 16px;
    line-height: 1.7;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.4);
}

.output-title {
    color: #38bdf8;
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 10px;
}

.tag {
    display: inline-block;
    background-color: #1e293b;
    color: #38bdf8;
    padding: 5px 12px;
    margin-right: 8px;
    border-radius: 20px;
    font-size: 12px;
}

.footer {
    text-align: center;
    margin-top: 40px;
    color: #64748b;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="main-title">🧠 GenCopy</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-powered marketing copy generator for small businesses</div>',
    unsafe_allow_html=True
)

# ---------------- INPUT SECTION ----------------
st.subheader("📥 Enter Product Details")

product = st.text_input("Product Name")
description = st.text_area("Product Description", height=120)
audience = st.text_input("Target Audience")
keywords = st.text_input("SEO Keywords (optional)")

col1, col2 = st.columns(2)

with col1:
    tone = st.selectbox(
        "Select Tone",
        ["Professional", "Persuasive", "Friendly"]
    )

with col2:
    content_type = st.selectbox(
        "Content Type",
        [
            "Product Description",
            "Social Media Post",
            "Promotional Email",
            "Ad Slogan"
        ]
    )

st.markdown("---")

# ---------------- GENERATE BUTTON ----------------
if st.button("✨ Generate Marketing Copy", use_container_width=True):

    if not product or not description or not audience:
        st.warning("⚠️ Please fill in all required fields.")
    else:
        with st.spinner("Generating high-quality marketing content..."):
            data = preprocess_inputs(product, description, audience, keywords)
            prompt = create_prompt(data, tone, content_type)
            output = generate_content(prompt)
            final_output = apply_rules(output, tone)

        st.success("Content generated successfully!")

        # ---------------- OUTPUT SECTION ----------------
        st.markdown(f"""
        <div class="output-box">
            <div class="output-title">✨ Generated Marketing Copy</div>

            <span class="tag">{tone}</span>
            <span class="tag">{content_type}</span>

            <br><br>
            {final_output.replace('\n', '<br>')}
        </div>
        """, unsafe_allow_html=True)

        # Copy-friendly block
        st.markdown("### 📋 Copy Text")
        st.code(final_output, language="markdown")

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
GenCopy • Built using Gemini 2.5 Flash • Streamlit • Generative AI
</div>
""", unsafe_allow_html=True)
