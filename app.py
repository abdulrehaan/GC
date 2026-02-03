from dotenv import load_dotenv
import os
import re
import streamlit as st
from io import BytesIO

# Load environment variables
load_dotenv()

from modules.preprocessing import preprocess_inputs
from modules.prompt_engineering import create_prompt
from modules.ai_generator import generate_content
from modules.rules import apply_rules
from modules.image_generator import generate_product_image

# ────────────────────────────────────────────────
# PAGE CONFIG
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="GenCopy – AI Marketing Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ────────────────────────────────────────────────
# MODERN PREMIUM DARK THEME + COLOR PALETTE
# ────────────────────────────────────────────────
st.markdown("""
<style>
    body, .stApp {
        background-color: #0a0e1a;
        color: #f1f5f9;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }

    .main-title {
        text-align: center;
        font-size: 52px;
        font-weight: 900;
        background: linear-gradient(90deg, #00d4ff, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 20px 0 8px;
    }

    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 20px;
        margin-bottom: 40px;
    }

    .output-box {
        background: linear-gradient(145deg, #111827 0%, #0f172a 100%);
        padding: 32px;
        border-radius: 20px;
        border: 1px solid #334155;
        margin: 24px 0;
        white-space: pre-wrap;
    }

    .output-title {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(90deg, #00eaff, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }

    .tag {
        display: inline-block;
        background: linear-gradient(90deg, #7c3aed, #00d4ff);
        color: white;
        padding: 8px 16px;
        margin: 0 10px 10px 0;
        border-radius: 50px;
        font-size: 14px;
        font-weight: 600;
    }

    .footer {
        text-align: center;
        margin: 60px 0 30px;
        color: #64748b;
        font-size: 15px;
        border-top: 1px solid #1e293b;
        padding-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# HEADER
# ────────────────────────────────────────────────
st.markdown('<div class="main-title">GenCopy</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-Powered Marketing Studio • Copy + Visuals • Built for Creators</div>',
    unsafe_allow_html=True
)

# ────────────────────────────────────────────────
# INPUT FORM
# ────────────────────────────────────────────────
st.markdown("### Enter Your Product Details")

with st.form(key="product_form", clear_on_submit=False):
    colA, colB = st.columns([3, 2])

    with colA:
        product = st.text_input("Product Name*", placeholder="e.g. Resistance Band Set")
        description = st.text_area(
            "Product Description*",
            height=130,
            placeholder="High-quality resistance bands with handles, door anchor, carry bag..."
        )
        audience = st.text_input("Target Audience*", placeholder="Home workout enthusiasts")
        keywords = st.text_input("SEO Keywords (optional)", placeholder="fitness, home gym")

    with colB:
        tone = st.selectbox("Tone", ["Professional", "Persuasive", "Friendly"], index=1)
        content_type = st.selectbox(
            "Content Type",
            ["Social Media Post", "Product Description", "Promotional Email", "Ad Slogan"],
            index=0
        )

    submit_button = st.form_submit_button(
        "✨ Generate Copy & Product Visual",
        use_container_width=True,
        type="primary"
    )

# ────────────────────────────────────────────────
# TEXT CLEANER
# ────────────────────────────────────────────────
def clean_generated_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"^```[\w]*\n?|```$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{4,}", "\n\n", text)
    return text.strip()

# ────────────────────────────────────────────────
# GENERATION LOGIC
# ────────────────────────────────────────────────
if submit_button:
    if not product or not description or not audience:
        st.error("Please complete Product Name, Description, and Target Audience.")
    else:
        with st.spinner("Crafting compelling copy & generating visual..."):
            try:
                data = preprocess_inputs(product, description, audience, keywords)
                prompt = create_prompt(data, tone, content_type)

                raw_output = generate_content(prompt)
                if raw_output.startswith("Groq API error"):
                    raise ValueError(raw_output)

                cleaned = clean_generated_text(raw_output)
                final_output = apply_rules(cleaned, tone)

                image = generate_product_image(product, data["description"])

                st.success("Generation complete!")

                col_text, col_image = st.columns([3, 2])

                with col_text:
                    st.markdown(f"""
                    <div class="output-box">
                        <div class="output-title">Generated {content_type}</div>
                        <span class="tag">{tone}</span>
                        <span class="tag">{content_type}</span>
                        <br><br>
                        {final_output.replace('\n', '<br>')}
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("#### 📋 Copy Text (ready to paste)")
                    st.code(final_output, language="markdown")

                with col_image:
                    st.markdown("#### Product Visual")
                    if image:
                        st.image(image, use_column_width=True)
                        buf = BytesIO()
                        image.save(buf, format="PNG")
                        st.download_button(
                            label="Download High-Res Image",
                            data=buf.getvalue(),
                            file_name=f"{product.replace(' ', '_')}.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    else:
                        st.info("Could not generate image – check Hugging Face API key.")

            except Exception as e:
                st.error(
                    f"Error during generation:\n{str(e)}\n\nPlease check API keys or try again."
                )

# ────────────────────────────────────────────────
# FOOTER
# ────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    GenCopy • AI Marketing Studio • Powered by Groq & Hugging Face • Hyderabad • 2026
</div>
""", unsafe_allow_html=True)
