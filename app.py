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
# NAVY BLUE DESIGN
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #F5F8FC;
}

.main-title {
    font-size: 48px;
    font-weight: 800;
    color: #0B1F3A;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 22px;
    color: #173B67;
}

.hero-small {
    font-size: 17px;
    color: #52657A;
}

.sidebar-title {
    font-size: 25px;
    font-weight: 800;
    color: #0B1F3A;
}

.feature-card {
    padding: 25px;
    border-radius: 18px;
    background: white;
    border: 1px solid #D7E0EA;
    min-height: 150px;
    text-align: center;
    box-shadow: 0 5px 18px rgba(11,31,58,0.08);
}

.feature-icon {
    font-size: 40px;
}

.feature-title {
    font-size: 21px;
    font-weight: 700;
    color: #0B1F3A;
}

.feature-text {
    color: #52657A;
}

.answer-box {
    padding: 15px;
    border-radius: 15px;
    background: #EAF2FF;
    border-left: 6px solid #0B1F3A;
    margin-top: 20px;
}

.tip-card {
    padding: 20px;
    border-radius: 15px;
    background: white;
    border: 1px solid #D7E0EA;
    min-height: 130px;
    box-shadow: 0 5px 18px rgba(11,31,58,0.06);
}

div.stButton > button {
    background-color: #0B1F3A;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 18px;
    font-weight: 700;
    min-height: 45px;
}

div.stButton > button:hover {
    background-color: #173B67;
    color: white;
    border: none;
}

div[data-testid="stTextArea"] textarea {
    border: 2px solid #B8C7D9;
    border-radius: 12px;
}

div[data-testid="stTextInput"] input {
    border: 2px solid #B8C7D9;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# IMAGE URLS
# --------------------------------------------------

student_image = (
    "https://images.unsplash.com/"
    "photo-1523240795612-9a054b0db644?"
    "auto=format&fit=crop&w=1000&q=85"
)

study_image = (
    "https://images.unsplash.com/"
    "photo-1434030216411-0b793f4b4173?"
    "auto=format&fit=crop&w=1000&q=85"
)

books_image = (
    "https://images.unsplash.com/"
    "photo-1495446815901-a7297e633e8d?"
    "auto=format&fit=crop&w=1000&q=85"
)

ai_image = (
    "https://images.unsplash.com/"
    "photo-1535378917042-10a22c95931a?"
    "auto=format&fit=crop&w=1000&q=85"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "selected_tool" not in st.session_state:
    st.session_state.selected_tool = "💬 Ask AI"

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div style="text-align:center;">

<div style="font-size:60px;">📚</div>

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

    st.markdown("### 🧠 Choose Your Tool")

    if st.button(
        "💬 Ask AI",
        use_container_width=True,
        key="side_ask"
    ):
        st.session_state.selected_tool = "💬 Ask AI"

    if st.button(
        "📖 Explain Topic",
        use_container_width=True,
        key="side_explain"
    ):
        st.session_state.selected_tool = "📖 Explain Topic"

    if st.button(
        "📝 Summarize Notes",
        use_container_width=True,
        key="side_summary"
    ):
        st.session_state.selected_tool = "📝 Summarize"

    if st.button(
        "🎯 Generate Quiz",
        use_container_width=True,
        key="side_quiz"
    ):
        st.session_state.selected_tool = "🎯 Generate Quiz"

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

    if st.button(
        "💬 Ask AI",
        use_container_width=True,
        key="feature_ask"
    ):
        st.session_state.selected_tool = "💬 Ask AI"
        st.rerun()

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

    if st.button(
        "📖 Explain Topic",
        use_container_width=True,
        key="feature_explain"
    ):
        st.session_state.selected_tool = "📖 Explain Topic"
        st.rerun()

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

    if st.button(
        "📝 Summarize",
        use_container_width=True,
        key="feature_summary"
    ):
        st.session_state.selected_tool = "📝 Summarize"
        st.rerun()

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

    if st.button(
        "🎯 Generate Quiz",
        use_container_width=True,
        key="feature_quiz"
    ):
        st.session_state.selected_tool = "🎯 Generate Quiz"
        st.rerun()

# --------------------------------------------------
# IMAGE SECTION
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
# SELECTED TOOL
# --------------------------------------------------

st.markdown("---")

selected_tool = st.session_state.selected_tool

st.markdown(
    f"## {selected_tool}"
)

# --------------------------------------------------
# ASK AI / EXPLAIN TOPIC
# --------------------------------------------------

if selected_tool in ["💬 Ask AI", "📖 Explain Topic"]:

    st.image(
        ai_image,
        caption="🤖 Your AI Study Partner",
        use_container_width=True
    )

    if selected_tool == "💬 Ask AI":

        question_label = "💭 Your Question"

        placeholder = (
            "Example: Explain Python variables "
            "in very simple language..."
        )

    else:

        question_label = "📖 Topic to Explain"

        placeholder = (
            "Example: Explain recursion in Python "
            "with an easy example..."
        )

    question = st.text_area(
        question_label,
        placeholder=placeholder,
        height=150,
        key="question_box"
    )

    if st.button(
        "🤖 Ask AI",
        use_container_width=True,
        key="main_ask_ai"
    ):

        if not question.strip():

            st.warning(
                "⚠️ Please enter your question first."
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

                <h2 style="color:#0B1F3A;">
                🤖 AI Tutor Answer
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
                    "Please add GEMINI_API_KEY "
                    "in Streamlit Secrets."
                )

            except Exception as e:

                st.error(
                    "❌ Something went wrong "
                    "while connecting to Gemini."
                )

                st.code(str(e))

# --------------------------------------------------
# SUMMARIZE
# --------------------------------------------------

elif selected_tool == "📝 Summarize":

    st.image(
        books_image,
        caption="📝 Turn your notes into simple revision points",
        use_container_width=True
    )

    st.markdown(
        "### 📝 Paste your notes below"
    )

    notes = st.text_area(
        "Your Notes",
        placeholder="Paste your study notes here...",
        height=220,
        key="notes_box"
    )

    if st.button(
        "✨ Summarize Notes",
        use_container_width=True,
        key="summarize_button"
    ):

        if not notes.strip():

            st.warning(
                "⚠️ Please enter your notes first."
            )

        else:

            try:

                api_key = st.secrets["GEMINI_API_KEY"]

                client = genai.Client(
                    api_key=api_key
                )

                prompt = f"""
Summarize these study notes.

Notes:

{notes}

Give the answer in this format:

### 📌 Key Concepts

### ⭐ Important Points

### 📝 Short Revision Notes

### ❓ Possible Exam Questions

Use very simple language.
"""

                with st.spinner(
                    "📝 Creating your summary..."
                ):

                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt
                    )

                st.markdown(
                    "## 📚 Your Summary"
                )

                st.markdown(response.text)

            except Exception as e:

                st.error(
                    "❌ Could not summarize notes."
                )

                st.code(str(e))

# --------------------------------------------------
# QUIZ
# --------------------------------------------------

elif selected_tool == "🎯 Generate Quiz":

    st.image(
        study_image,
        caption="🎯 Practice your knowledge with AI-generated questions",
        use_container_width=True
    )

    st.markdown(
        "### 🎯 Generate a Practice Quiz"
    )

    quiz_topic = st.text_input(
        "📚 Enter your topic",
        placeholder="Example: Python Basics",
        key="quiz_topic_box"
    )

    if st.button(
        "🚀 Generate Quiz",
        use_container_width=True,
        key="generate_quiz_button"
    ):

        if not quiz_topic.strip():

            st.warning(
                "⚠️ Please enter a topic first."
            )

        else:

            try:

                api_key = st.secrets["GEMINI_API_KEY"]

                client = genai.Client(
                    api_key=api_key
                )

                prompt = f"""
Create a beginner-friendly quiz.

Topic:

{quiz_topic}

Create 10 multiple-choice questions.

For every question provide:

Question

A. Option
B. Option
C. Option
D. Option

Then provide the correct answer.

Also provide a short explanation
for each answer.
"""

                with st.spinner(
                    "🎯 Creating your quiz..."
                ):

                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt
                    )

                st.markdown(
                    "## 🎯 Your Practice Quiz"
                )

                st.markdown(response.text)

            except Exception as e:

                st.error(
                    "❌ Could not generate quiz."
                )

                st.code(str(e))

# --------------------------------------------------
# SMART STUDY TIPS
# --------------------------------------------------

st.markdown("---")

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

<h3 style="color:#0B1F3A;">
📚 AI Study Assistant
</h3>

<p>
Made with 🐍 Python • 🎨 Streamlit • 🤖 Gemini AI
</p>

<p>
💬 Learn • 📖 Practice • 📝 Revise • 🎯 Succeed 🚀
</p>

</div>
""", unsafe_allow_html=True)
