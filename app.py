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
    background: linear-gradient(135deg, #f8faff, #eef2ff);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Header */
.hero {
    background: linear-gradient(135deg, #312e81, #4f46e5, #7c3aed);
    padding: 38px 30px;
    border-radius: 28px;
    text-align: center;
    color: white;
    box-shadow: 0 12px 35px rgba(79, 70, 229, 0.25);
    margin-bottom: 30px;
}

.hero-icon {
    font-size: 55px;
}

.hero h1 {
    font-size: 44px;
    margin: 5px 0;
    font-weight: 800;
}

.hero p {
    font-size: 19px;
    margin: 8px;
}

.hero-small {
    font-size: 15px !important;
    opacity: 0.9;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #eef2ff, #f5f3ff);
}

.sidebar-title {
    background: linear-gradient(135deg, #312e81, #6366f1);
    color: white;
    padding: 18px;
    border-radius: 16px;
    text-align: center;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 20px;
}

/* Section titles */
.section-title {
    color: #312e81;
    font-size: 28px;
    font-weight: 800;
    margin-top: 25px;
    margin-bottom: 18px;
}

/* Feature cards */
.feature-card {
    background: white;
    padding: 25px 18px;
    border-radius: 20px;
    text-align: center;
    min-height: 155px;
    border: 1px solid #e0e7ff;
    box-shadow: 0 6px 20px rgba(30, 41, 59, 0.08);
    transition: 0.2s;
}

.feature-icon {
    font-size: 38px;
    margin-bottom: 8px;
}

.feature-title {
    color: #312e81;
    font-size: 19px;
    font-weight: 700;
}

.feature-text {
    color: #64748b;
    font-size: 14px;
    margin-top: 8px;
}

/* Tutor box */
.tutor-box {
    background: linear-gradient(135deg, #eef2ff, #f5f3ff);
    padding: 28px;
    border-radius: 24px;
    border: 1px solid #c7d2fe;
    margin-top: 30px;
    margin-bottom: 20px;
}

.tutor-title {
    color: #312e81;
    font-size: 30px;
    font-weight: 800;
}

/* Answer */
.answer-box {
    background: linear-gradient(135deg, #ecfdf5, #eff6ff);
    padding: 20px;
    border-radius: 20px;
    border-left: 6px solid #4f46e5;
    margin-top: 25px;
}

/* Tips */
.tip-card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #e2e8f0;
    min-height: 145px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.06);
}

.tip-title {
    color: #312e81;
    font-size: 18px;
    font-weight: 700;
}

.tip-text {
    color: #64748b;
    font-size: 14px;
}

/* Buttons */
.stButton > button {
    border-radius: 14px;
    border: none;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    font-weight: 700;
    padding: 10px 20px;
    min-height: 48px;
    box-shadow: 0 5px 15px rgba(79,70,229,0.2);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #3730a3, #6d28d9);
    color: white;
}

/* Footer */
.footer {
    margin-top: 45px;
    padding: 30px;
    text-align: center;
    background: linear-gradient(135deg, #312e81, #4f46e5);
    color: white;
    border-radius: 22px;
}

.footer-title {
    font-size: 24px;
    font-weight: 800;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero">

<div class="hero-icon">📚</div>

<h1>AI Study Assistant</h1>

<p>Your personal AI tutor 🤖</p>

<p class="hero-small">
✨ Learn &nbsp; • &nbsp;
💡 Understand &nbsp; • &nbsp;
📝 Practice &nbsp; • &nbsp;
🎯 Succeed
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

    st.info("💬 **Ask AI**\n\nAsk any study question.")

    st.success("📖 **Explain Topic**\n\nUnderstand difficult topics.")

    st.warning("📝 **Summarize**\n\nGet simple notes.")

    st.error("🎯 **Generate Quiz**\n\nPractice your knowledge.")

    st.markdown("---")

    st.markdown("### 🌟 Features")

    st.markdown("""
    📚 Easy explanations

    🤖 AI-powered answers

    💡 Simple language

    📝 Study-friendly notes

    🎯 Exam preparation

    🚀 Beginner friendly
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
    <div class="feature-card">

    <div class="feature-icon">💬</div>

    <div class="feature-title">
    Ask AI
    </div>

    <div class="feature-text">
    Ask questions about your subjects.
    </div>

    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="feature-card">

    <div class="feature-icon">📖</div>

    <div class="feature-title">
    Explain
    </div>

    <div class="feature-text">
    Understand difficult concepts easily.
    </div>

    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown("""
    <div class="feature-card">

    <div class="feature-icon">📝</div>

    <div class="feature-title">
    Summarize
    </div>

    <div class="feature-text">
    Turn long topics into simple notes.
    </div>

    </div>
    """, unsafe_allow_html=True)

with col4:

    st.markdown("""
    <div class="feature-card">

    <div class="feature-icon">🎯</div>

    <div class="feature-title">
    Practice
    </div>

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

st.caption("👩‍🎓 Study smarter • Ask questions • Improve every day 🚀")

# --------------------------------------------------
# AI TUTOR
# --------------------------------------------------

st.markdown("""
<div class="tutor-box">

<div class="tutor-title">
🤖 Ask Your AI Tutor
</div>

<p>
💭 Don't understand a topic? No problem!
Ask your AI tutor and get a simple explanation.
</p>

<p>
🎓 You can ask about Python, Maths, Science, Engineering,
or any other study topic.
</p>

</div>
""", unsafe_allow_html=True)

question = st.text_area(
    "💭 Your Question",
    placeholder="✨ Example: Explain Python variables in very simple language...",
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

            <h2 style="color:#312e81;">
            📖 AI Tutor Answer 🤖
            </h2>

            <p>
            ✨ Here is your easy-to-understand answer:
            </p>

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
    <div class="tip-card">

    <div class="tip-title">
    ⏰ Study Regularly
    </div>

    <div class="tip-text">
    Study for a small amount of time every day
    instead of studying everything at the last moment.
    </div>

    </div>
    """, unsafe_allow_html=True)

with tip2:

    st.markdown("""
    <div class="tip-card">

    <div class="tip-title">
    🧠 Practice More
    </div>

    <div class="tip-text">
    Practice questions regularly to improve
    your understanding and confidence.
    </div>

    </div>
    """, unsafe_allow_html=True)

with tip3:

    st.markdown("""
    <div class="tip-card">

    <div class="tip-title">
    🔄 Revise
    </div>

    <div class="tip-text">
    Revise important concepts frequently
    so you can remember them for longer.
    </div>

    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">

<div class="footer-title">
📚 AI Study Assistant 🤖
</div>

<p>
Your personal AI tutor for smarter learning ✨
</p>

<p>
🐍 Python &nbsp; • &nbsp;
🎨 Streamlit &nbsp; • &nbsp;
🤖 Gemini AI
</p>

<p>
💬 Learn &nbsp; • &nbsp;
📖 Practice &nbsp; • &nbsp;
🎯 Revise &nbsp; • &nbsp;
🏆 Succeed
</p>

<p>
❤️ Made for students
</p>

</div>
""", unsafe_allow_html=True)
