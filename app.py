from dotenv import load_dotenv
import os
import re
import streamlit as st
from io import BytesIO

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
    /* Global */
    body, .stApp {
        background-color: #0a0e1a;
        color: #f1f5f9;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }

    /* Titles & Headers */
    .main-title {
        text-align: center;
        font-size: 52px;
        font-weight: 900;
        background: linear-gradient(90deg, #00d4ff, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 20px 0 8px;
        letter-spacing: -1px;
    }
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 20px;
        margin-bottom: 40px;
        font-weight: 400;
    }

    /* Input Form */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #111827;
        color: #f1f5f9;
        border: 1px solid #374151;
        border-radius: 10px;
        padding: 12px;
    }
    .stSelectbox > div > div > select {
        background-color: #111827;
        color: #f1f5f9;
        border: 1px solid #374151;
    }

    /* Output Box – Premium Card Look */
    .output-box {
        background: linear-gradient(145deg, #111827 0%, #0f172a 100%);
        padding: 32px;
        border-radius: 20px;
        border: 1px solid #334155;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5),
                    inset 0 0 20px rgba(0, 212, 255, 0.08);
        color: #f1f5f9;
        font-size: 16.5px;
        line-height: 1.85;
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

    /* Tags */
    .tag {
        display: inline-block;
        background: linear-gradient(90deg, #7c3aed, #00d4ff);
        color: white;
        padding: 8px 16px;
        margin: 0 10px 10px 0;
        border-radius: 50px;
        font-size: 14px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0, 212, 255, 0.25);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00d4ff, #7c3aed);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 14px 32px;
        font-size: 16px;
        font-weight: 700;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(0, 212, 255, 0.4);
    }

    /* Image */
    .stImage {
        border-radius: 16px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
        border: 1px solid #334155;
        transition: transform 0.3s;
    }
    .stImage:hover {
        transform: scale(1.02);
    }

    /* Footer */
    .footer {
        text-align: center;
        margin: 60px 0 30px;
        color: #64748b;
        font-size: 15px;
        padding-top: 30px;
        border-top: 1px solid #1e293b;
    }

    /* Success/Error */
    .stSuccess {
        background-color: #064e3b !important;
        color: #a7f3d0 !important;
    }
    .stError {
        background-color: #7f1d1d !important;
        color: #fecaca !important;
    }
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# HEADER
# ────────────────────────────────────────────────
st.markdown('<div class="main-title">GenCopy</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Powered Marketing Studio • Copy + Visuals • Built for Creators</div>', unsafe_allow_html=True)

# ────────────────────────────────────────────────
# INPUT FORM – centered and clean
# ────────────────────────────────────────────────
st.markdown("### Enter Your Product Details")

with st.form(key="product_form", clear_on_submit=False):
    colA, colB = st.columns([3, 2])

    with colA:
        product = st.text_input("Product Name*", placeholder="e.g. Resistance Band Set with Handles & Door Anchor")
        description = st.text_area("Product Description*", height=130,
                                  placeholder="5 latex bands, total 1040 kg resistance, non-slip handles, door anchor, carry bag, workout PDF...")
        audience = st.text_input("Target Audience*", placeholder="e.g. home workout enthusiasts, beginners to intermediate")
        keywords = st.text_input("SEO Keywords (optional)", placeholder="resistance bands, home gym, fitness accessories india")

    with colB:
        tone = st.selectbox("Tone", ["Professional", "Persuasive", "Friendly"], index=1)
        content_type = st.selectbox("Content Type", [
            "Social Media Post",
            "Product Description",
            "Promotional Email",
            "Ad Slogan"
        ], index=0)

    submit_button = st.form_submit_button("✨ Generate Copy & Product Visual", use_container_width=True, type="primary")

# ────────────────────────────────────────────────
# CLEANING FUNCTION
# ────────────────────────────────────────────────
def clean_generated_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'^```[\w]*\n?|```$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{4,}', '\n\n', text)
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
<<<<<<< HEAD
                if raw_output.startswith("Groq API error"):
                    raise ValueError(raw_output)


=======
                if "failed" in raw_output.lower():
                    raise ValueError(raw_output)

>>>>>>> 259735af47a4dd1ddfd0685fe05e84ceec63cc34
                cleaned = clean_generated_text(raw_output)
                final_output = apply_rules(cleaned, tone)

                image = generate_product_image(product, data['description'])

                st.success("Generation complete!")

                # ── Two-column layout: Text + Image ──
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

<<<<<<< HEAD
                    #st.markdown("#### 📋 Copy Text (ready to paste)")
                    #st.code(final_output, language="markdown")
=======
                    st.markdown("#### 📋 Copy Text (ready to paste)")
                    st.code(final_output, language="markdown")
>>>>>>> 259735af47a4dd1ddfd0685fe05e84ceec63cc34

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
                st.error(f"Error during generation:\n{str(e)}\n\nPlease check API keys or try again.")

# ────────────────────────────────────────────────
# FOOTER
# ────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    GenCopy • AI Marketing Studio • Powered by Gemini & Stable Diffusion • Hyderabad • 2026
</div>
""", unsafe_allow_html=True)