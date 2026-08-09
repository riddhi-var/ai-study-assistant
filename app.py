import streamlit as st
from google import genai

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(124, 58, 237, 0.18), transparent 28%),
        radial-gradient(circle at 90% 10%, rgba(14, 165, 233, 0.18), transparent 25%),
        linear-gradient(135deg, #f8fafc 0%, #eef2ff 50%, #f0fdfa 100%);
}

/* Main container */
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Header */
.hero {
    padding: 35px 30px;
    border-radius: 28px;
    background: linear-gradient(135deg, #312e81, #6d28d9, #0f766e);
    color: white;
    text-align: center;
    box-shadow: 0 18px 45px rgba(49, 46, 129, 0.25);
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 45px;
    margin-bottom: 8px;
    font-weight: 800;
}

.hero p {
    font-size: 18px;
    margin: 5px;
}

.hero-small {
    font-size: 14px;
    opacity: 0.9;
}

/* Section title */
.section-title {
    font-size: 27px;
    font-weight: 800;
    color: #312e81;
    margin-top: 20px;
    margin-bottom: 15px;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.88);
    padding: 22px;
    border-radius: 20px;
    border: 1px solid rgba(99,102,241,0.12);
    box-shadow: 0 10px 28px rgba(15,23,42,0.08);
    min-height: 150px;
    margin-bottom: 15px;
}

.card h3 {
    color: #312e81;
    margin-bottom: 8px;
}

.card p {
    color: #475569;
    line-height: 1.6;
}

/* Ask area */
.ask-box {
    background: white;
    padding: 28px;
    border-radius: 25px;
    box-shadow: 0 15px 40px rgba(15,23,42,0.10);
    border: 1px solid #e0e7ff;
    margin-top: 10px;
    margin-bottom: 25px;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: none;
    padding: 12px 18px;
    font-weight: 700;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    box-shadow: 0 7px 18px rgba(79,70,229,0.22);
    transition: 0.2s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(79,70,229,0.30);
}

/* Text input */
.stTextArea textarea {
    border-radius: 15px !important;
    border: 2px solid #c7d2fe !important;
    background: #fafaff !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e1b4b, #312e81, #164e63);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.sidebar-title {
    text-align: center;
    font-size: 23px;
    font-weight: 800;
    margin-bottom: 20px;
}

/* Answer */
.answer-box {
    background: white;
    padding: 28px;
    border-radius: 22px;
    border-left: 6px solid #6366f1;
    box-shadow: 0 10px 30px rgba(15,23,42,0.08);
    margin-top: 20px;
}

/* Feature cards */
.feature {
    text-align: center;
    padding: 22px 15px;
    background: rgba(255,255,255,0.9);
    border-radius: 20px;
    box-shadow: 0 8px 25px rgba(15,23,42,0.07);
    min-height: 145px;
}

.feature-icon {
    font-size: 38px;
}

.feature-title {
    font-weight: 800;
    color: #312e81;
    margin-top: 8px;
}

.feature-text {
    font-size: 14px;
    color: #64748b;
}

/* Footer */
.footer {
    text-align: center;
    color: #64748b;
    margin-top: 35px;
    padding: 20px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero">

    <div style="font-size:55px;">📚</div>

    <h1>AI Study Assistant</h1>

    <p>Your personal AI tutor 🤖</p>

    <p class="hero-small">
        Learn • Practice • Revise • Succeed ✨
    </p>

</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🎓 Study Center</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 🧠 Study Tools")

    st.info("💬 Ask AI\n\nAsk any study question.")

    st.success("📖 Explain Topic\n\nUnderstand difficult topics.")

    st.warning("📝 Summarize\n\nGet simple notes.")

    st.error("🎯 Generate Quiz\n\nPractice your knowledge.")

    st.markdown("---")

    st.markdown("### 🌟 Features")

    st.markdown("""
    📚 Easy explanations

    🤖 AI-powered answers

    💡 Simple language

    📝 Study-friendly notes

    🎯 Exam preparation
    """)

    st.markdown("---")

    st.caption("Made with ❤️ using Python + Streamlit + Gemini")

# --------------------------------------------------
# FEATURE SECTION
# --------------------------------------------------

st.markdown(
    '<div class="section-title">✨ What can I help you with?</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature">
        <div class="feature-icon">💬</div>
        <div class="feature-title">Ask AI</div>
        <div class="feature-text">
            Ask questions about your subjects.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature">
        <div class="feature-icon">📖</div>
        <div class="feature-title">Explain</div>
        <div class="feature-text">
            Understand difficult concepts easily.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature">
        <div class="feature-icon">📝</div>
        <div class="feature-title">Summarize</div>
        <div class="feature-text">
            Turn long topics into simple notes.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">Practice</div>
        <div class="feature-text">
            Generate questions for revision.
        </div>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# IMAGE / STUDY BANNER
# --------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

st.image(
    "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1600&q=85",
    use_container_width=True
)

# --------------------------------------------------
# AI TUTOR
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🤖 Ask Your AI Tutor</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="ask-box">

<h3 style="color:#312e81;">
💡 Ask me anything about your studies
</h3>

<p style="color:#64748b;">
I can explain programming, mathematics, science,
engineering and many other subjects in simple language.
</p>

</div>
""", unsafe_allow_html=True)

question = st.text_area(
    "💭 Your Question",
    placeholder="Example: Explain Python variables in very simple language...",
    height=150
)

# --------------------------------------------------
# ASK AI BUTTON
# --------------------------------------------------

if st.button("🤖  Ask AI", use_container_width=True):

    if not question.strip():

        st.warning("⚠️ Please enter a question first.")

    else:

        try:

            # Read Gemini API key from Streamlit Secrets
            api_key = st.secrets["GEMINI_API_KEY"]

            client = genai.Client(api_key=api_key)

            prompt = f"""
You are an AI Study Assistant.

The student asked:

{question}

Answer in very simple language.

Follow this structure:

### 📖 Simple Explanation

Explain the concept clearly.

### 💡 Example

Give an easy example.

### 📝 Important Points

Give 3 to 5 important points.

### 🎯 Quick Revision

Give a short revision summary.

Use emojis where helpful.
Avoid unnecessarily complicated words.
"""

            with st.spinner("🤖 AI is preparing your answer..."):

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

            st.markdown("""
            <div class="answer-box">
            <h2 style="color:#312e81;">📖 AI Tutor Answer</h2>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(response.text)

            st.success("✅ Done! Keep learning 🚀")

        except KeyError:

            st.error(
                "🔐 Gemini API key is missing. "
                "Please add GEMINI_API_KEY in Streamlit Secrets."
            )

        except Exception as e:

            st.error("❌ Something went wrong while connecting to Gemini.")

            st.code(str(e))

# --------------------------------------------------
# STUDY TIPS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🌟 Smart Study Tips</div>',
    unsafe_allow_html=True
)

tip1, tip2, tip3 = st.columns(3)

with tip1:
    st.markdown("""
    <div class="card">
        <h3>⏰ Study Regularly</h3>
        <p>
        Study for a small amount of time every day
        instead of studying everything at the last moment.
        </p>
    </div>
    """, unsafe_allow_html=True)

with tip2:
    st.markdown("""
    <div class="card">
        <h3>🧠 Practice More</h3>
        <p>
        Practice questions regularly to improve
        your understanding and confidence.
        </p>
    </div>
    """, unsafe_allow_html=True)

with tip3:
    st.markdown("""
    <div class="card">
        <h3>🔄 Revise</h3>
        <p>
        Revise important concepts frequently
        so you can remember them for longer.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">

📚 <b>AI Study Assistant</b>

<br>

Made with 🐍 Python • 🎨 Streamlit • 🤖 Gemini AI

<br><br>

Learn • Practice • Revise • Succeed 🚀

</div>
""", unsafe_allow_html=True)
