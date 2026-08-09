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

.main-title {
    font-size: 48px;
    font-weight: 800;
    color: #312e81;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 22px;
    color: #6366f1;
}

.hero-small {
    font-size: 17px;
    color: #64748b;
}

.feature-card {
    padding: 25px;
    border-radius: 18px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    min-height: 150px;
    text-align: center;
}

.feature-icon {
    font-size: 40px;
}

.feature-title {
    font-size: 21px;
    font-weight: 700;
    color: #312e81;
}

.feature-text {
    color: #475569;
}

.answer-box {
    padding: 15px;
    border-radius: 15px;
    background: #eef2ff;
    margin-top: 20px;
}

.tip-card {
    padding: 20px;
    border-radius: 15px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    min-height: 130px;
}

.sidebar-title {
    font-size: 25px;
    font-weight: 800;
    color: #312e81;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# IMAGE URLS
# --------------------------------------------------

student_image = "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=900&q=85"

study_image = "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=900&q=85"

books_image = "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?auto=format&fit=crop&w=900&q=85"

ai_image = "https://images.unsplash.com/photo-1535378917042-10a22c95931a?auto=format&fit=crop&w=900&q=85"

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div style="text-align:center;">

<div style="font-size:55px;">📚</div>

<div class="main-title">
AI Study Assistant
</div>

<div class="subtitle">
Your personal AI tutor 🤖
</div>

<div class="hero-small">
Learn • Practice • Revise • Succeed ✨
</div>

</div>
""", unsafe_allow_html=True)

st.write("")

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

    st.caption(
        "Made with ❤️ using Python + Streamlit + Gemini"
    )

# --------------------------------------------------
# FEATURE SECTION
# --------------------------------------------------

st.markdown(
    "## ✨ What can I help you with?"
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
# STUDY IMAGE SECTION
# --------------------------------------------------

st.write("")

image1, image2, image3 = st.columns(3)

with image1:

    st.image(
        student_image,
        caption="🧑‍🎓 Ask your doubts and learn",
        use_container_width=True
    )

with image2:

    st.image(
        study_image,
        caption="📖 Learn smarter every day",
        use_container_width=True
    )

with image3:

    st.image(
        books_image,
        caption="📚 Build your knowledge",
        use_container_width=True
    )

# --------------------------------------------------
# AI TUTOR
# --------------------------------------------------

st.markdown(
    "## 🤖 Ask Your AI Tutor"
)

st.image(
    ai_image,
    caption="🤖 Your AI Study Partner",
    use_container_width=True
)

question = st.text_area(
    "💭 Your Question",
    placeholder="Example: Explain Python variables in very simple language...",
    height=150
)

# --------------------------------------------------
# ASK AI BUTTON
# --------------------------------------------------

if st.button(
    "🤖  Ask AI",
    use_container_width=True
):

    if not question.strip():

        st.warning(
            "⚠️ Please enter a question first."
        )

    else:

        try:

            api_key = st.secrets["GEMINI_API_KEY"]

            client = genai.Client(
                api_key=api_key
            )

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

            with st.spinner(
                "🤖 AI is preparing your answer..."
            ):

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

            st.markdown("""
            <div class="answer-box">

            <h2 style="color:#312e81;">
            📖 AI Tutor Answer
            </h2>

            </div>
            """, unsafe_allow_html=True)

            st.markdown(response.text)

            st.success(
                "✅ Done! Keep learning 🚀"
            )

        except KeyError:

            st.error(
                "🔐 Gemini API key is missing. "
                "Please add GEMINI_API_KEY in Streamlit Secrets."
            )

        except Exception as e:

            st.error(
                "❌ Something went wrong while connecting to Gemini."
            )

            st.code(str(e))

# --------------------------------------------------
# STUDY TIPS
# --------------------------------------------------

st.markdown(
    "## 🌟 Smart Study Tips"
)

tip1, tip2, tip3 = st.columns(3)

with tip1:

    st.markdown("""
    <div class="tip-card">

    <h3>⏰ Study Regularly</h3>

    Study for a small amount of time every day
    instead of studying everything at the last moment.

    </div>
    """, unsafe_allow_html=True)

with tip2:

    st.markdown("""
    <div class="tip-card">

    <h3>🧠 Practice More</h3>

    Practice questions regularly to improve
    your understanding and confidence.

    </div>
    """, unsafe_allow_html=True)

with tip3:

    st.markdown("""
    <div class="tip-card">

    <h3>🔄 Revise</h3>

    Revise important concepts frequently
    so you can remember them for longer.

    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown("""
<div style="text-align:center; padding:25px;">

<h3>📚 AI Study Assistant</h3>

<p>
Made with 🐍 Python • 🎨 Streamlit • 🤖 Gemini AI
</p>

<p>
💬 Learn • 📖 Practice • 📝 Revise • 🎯 Succeed 🚀
</p>

</div>
""", unsafe_allow_html=True)
