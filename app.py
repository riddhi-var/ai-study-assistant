import streamlit as st
from google import genai
from pypdf import PdfReader
import time

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #eef4ff 0%, #f8fbff 50%, #eaf2ff 100%);
}

/* Main container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* Header */
.hero {
    background: linear-gradient(135deg, #071a52, #123b8f, #1769aa);
    padding: 42px 30px;
    border-radius: 28px;
    text-align: center;
    color: white;
    box-shadow: 0 15px 40px rgba(7, 26, 82, 0.25);
    margin-bottom: 30px;
    animation: fadeIn 1s ease;
}

.hero h1 {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero p {
    font-size: 18px;
    margin: 5px;
}

.hero-icon {
    font-size: 60px;
    animation: float 3s ease-in-out infinite;
}

/* Cards */
.card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    min-height: 175px;
    border: 1px solid #dce7ff;
    box-shadow: 0 8px 25px rgba(25, 55, 110, 0.08);
    transition: all 0.3s ease;
    margin-bottom: 20px;
}

.card:hover {
    transform: translateY(-7px);
    box-shadow: 0 15px 35px rgba(25, 55, 110, 0.18);
    border-color: #3978d4;
}

.card-icon {
    font-size: 40px;
}

.card-title {
    color: #071a52;
    font-size: 21px;
    font-weight: 700;
}

.card-text {
    color: #52627a;
    font-size: 14px;
}

/* Section titles */
.section-title {
    color: #071a52;
    font-size: 27px;
    font-weight: 800;
    margin-top: 25px;
    margin-bottom: 18px;
}

/* Answer box */
.answer-box {
    background: linear-gradient(135deg, #ffffff, #eef5ff);
    border-left: 6px solid #1769aa;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(25, 55, 110, 0.1);
    margin-top: 20px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #06143d, #09245c, #0d367d);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.sidebar-title {
    font-size: 25px;
    font-weight: 800;
    text-align: center;
    padding: 15px;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: 1px solid #b9cdf0;
    background: white;
    color: #071a52;
    font-weight: 700;
    padding: 11px;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    background: #071a52;
    color: white;
    border-color: #071a52;
    transform: translateY(-2px);
}

/* Primary button */
button[kind="primary"] {
    background: linear-gradient(135deg, #071a52, #1769aa) !important;
    color: white !important;
}

/* Inputs */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    border-radius: 14px !important;
    border: 1px solid #c5d5ef !important;
}

/* Footer */
.footer {
    margin-top: 45px;
    padding: 30px;
    text-align: center;
    background: #071a52;
    color: white;
    border-radius: 22px;
}

/* Animations */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(15px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes float {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-10px);
    }
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# GEMINI CLIENT
# ============================================================

if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔐 Gemini API key is missing.")
    st.info(
        "Go to Streamlit → Manage app → Settings → Secrets "
        "and add GEMINI_API_KEY."
    )
    st.stop()

try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("❌ Could not connect to Gemini.")
    st.code(str(e))
    st.stop()

MODEL = "gemini-2.5-flash"

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">
    <div class="hero-icon">📚</div>
    <h1>AI Study Assistant</h1>
    <p>Your Personal AI Tutor 🤖</p>
    <p>Learn • Practice • Revise • Succeed 🚀</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🎓 Study Center</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 🧠 Study Tools")

    tool = st.radio(
        "Choose a tool:",
        [
            "💬 Ask AI",
            "📖 Explain Topic",
            "📝 Summarize Notes",
            "🎯 Generate Quiz",
            "📄 Study PDF",
            "📅 Study Planner",
            "🧠 Flashcards",
            "🧮 Calculator",
            "⏱️ Study Timer"
        ]
    )

    st.markdown("---")

    st.markdown("### 🌟 Features")

    st.markdown("""
    📚 Simple explanations

    🤖 AI-powered learning

    💡 Beginner-friendly answers

    📝 Revision notes

    🎯 Exam preparation

    🧠 Practice tools
    """)

    st.markdown("---")
    st.caption("🐍 Python • 🎈 Streamlit • 🤖 Gemini")

# ============================================================
# FEATURE CARDS
# ============================================================

st.markdown(
    '<div class="section-title">✨ What can I help you with?</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

cards = [
    ("💬", "Ask AI", "Ask questions about your subjects."),
    ("📖", "Explain", "Understand difficult concepts easily."),
    ("📝", "Summarize", "Turn long topics into simple notes."),
    ("🎯", "Practice", "Generate questions for revision.")
]

for col, card in zip([col1, col2, col3, col4], cards):
    with col:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-icon">{card[0]}</div>
                <div class="card-title">{card[1]}</div>
                <div class="card-text">{card[2]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================================
# IMAGE
# ============================================================

st.image(
    "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1600&q=85",
    use_container_width=True
)

# ============================================================
# GEMINI FUNCTION
# ============================================================

def ask_gemini(prompt):

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text

# ============================================================
# ASK AI
# ============================================================

if tool == "💬 Ask AI":

    st.markdown(
        '<div class="section-title">🤖 Ask Your AI Tutor</div>',
        unsafe_allow_html=True
    )

    question = st.text_area(
        "💭 Your Question",
        placeholder="Example: Explain Python variables in very simple language...",
        height=150
    )

    if st.button("🤖 Ask AI", type="primary"):

        if not question.strip():
            st.warning("⚠️ Please enter your question first.")

        else:

            prompt = f"""
You are a friendly AI Study Assistant.

Student question:
{question}

Answer in very simple language.

Use this structure:

## 📖 Simple Explanation

## 💡 Example

## ⭐ Important Points

## 🎯 Quick Revision

Use emojis where useful.
Avoid unnecessarily complicated words.
"""

            with st.spinner("🤖 Your AI tutor is thinking..."):

                try:
                    answer = ask_gemini(prompt)

                    st.markdown(
                        '<div class="answer-box"><h2>📖 AI Tutor Answer</h2></div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(answer)
                    st.success("✅ Done! Keep learning 🚀")

                except Exception as e:
                    st.error("❌ Gemini could not answer right now.")
                    st.code(str(e))

# ============================================================
# EXPLAIN TOPIC
# ============================================================

elif tool == "📖 Explain Topic":

    st.markdown(
        '<div class="section-title">📖 Explain Any Topic</div>',
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "📚 Enter topic",
        placeholder="Example: Recursion in Python"
    )

    level = st.selectbox(
        "🎓 Explanation level",
        ["Beginner", "School Student", "College Student", "Exam Preparation"]
    )

    if st.button("📖 Explain Topic", type="primary"):

        if not topic.strip():
            st.warning("⚠️ Enter a topic first.")

        else:

            prompt = f"""
Explain the topic "{topic}" to a {level} student.

Use:

## 📖 Simple Explanation
## 💡 Easy Example
## ⭐ Important Points
## 📝 Exam Tip
## 🎯 Quick Revision

Use simple language.
"""

            with st.spinner("📖 Preparing explanation..."):

                try:
                    st.markdown(ask_gemini(prompt))
                except Exception as e:
                    st.error("❌ Could not explain the topic.")
                    st.code(str(e))

# ============================================================
# SUMMARIZE NOTES
# ============================================================

elif tool == "📝 Summarize Notes":

    st.markdown(
        '<div class="section-title">📝 Smart Notes Summarizer</div>',
        unsafe_allow_html=True
    )

    notes = st.text_area(
        "📄 Paste your notes",
        placeholder="Paste your study material here...",
        height=250
    )

    if st.button("✨ Summarize Notes", type="primary"):

        if not notes.strip():
            st.warning("⚠️ Please paste some notes.")

        else:

            prompt = f"""
Summarize these study notes:

{notes}

Give:

## 📌 Key Concepts
## ⭐ Important Points
## 📝 Short Revision Notes
## ❓ Possible Exam Questions

Use very simple language.
"""

            with st.spinner("📝 Creating your summary..."):

                try:
                    st.markdown(ask_gemini(prompt))
                except Exception as e:
                    st.error("❌ Could not summarize notes.")
                    st.code(str(e))

# ============================================================
# QUIZ
# ============================================================

elif tool == "🎯 Generate Quiz":

    st.markdown(
        '<div class="section-title">🎯 Quiz Generator</div>',
        unsafe_allow_html=True
    )

    quiz_topic = st.text_input(
        "📚 Quiz topic",
        placeholder="Example: Python Basics"
    )

    difficulty = st.selectbox(
        "🎚️ Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    number = st.slider(
        "🔢 Number of questions",
        5,
        15,
        10
    )

    if st.button("🚀 Generate Quiz", type="primary"):

        if not quiz_topic.strip():
            st.warning("⚠️ Enter a topic first.")

        else:

            prompt = f"""
Create a {number}-question multiple-choice quiz.

Topic: {quiz_topic}
Difficulty: {difficulty}

For every question provide:

Question
A.
B.
C.
D.

Then give the correct answer and a short explanation.

Keep formatting clear.
"""

            with st.spinner("🎯 Creating your quiz..."):

                try:
                    st.markdown(ask_gemini(prompt))
                except Exception as e:
                    st.error("❌ Could not generate quiz.")
                    st.code(str(e))

# ============================================================
# PDF STUDY
# ============================================================

elif tool == "📄 Study PDF":

    st.markdown(
        '<div class="section-title">📄 Study From Your PDF</div>',
        unsafe_allow_html=True
    )

    uploaded_pdf = st.file_uploader(
        "📚 Upload your study PDF",
        type=["pdf"]
    )

    if uploaded_pdf:

        try:

            reader = PdfReader(uploaded_pdf)
            text = ""

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

            st.success(
                f"✅ PDF loaded! {len(reader.pages)} page(s) found."
            )

            pdf_question = st.text_area(
                "💭 Ask a question about your PDF",
                placeholder="Example: What are the main points?"
            )

            if st.button("🤖 Ask PDF", type="primary"):

                if not pdf_question.strip():
                    st.warning("⚠️ Ask a question first.")

                else:

                    prompt = f"""
You are a study assistant.

Use the following PDF content to answer the student's question.

PDF content:
{text[:30000]}

Student question:
{pdf_question}

Answer in simple language.
If the information is not available in the PDF, say so.
"""

                    with st.spinner("📚 Reading your PDF..."):

                        try:
                            st.markdown(ask_gemini(prompt))
                        except Exception as e:
                            st.error("❌ Could not process the PDF.")
                            st.code(str(e))

        except Exception as e:
            st.error("❌ Could not read this PDF.")
            st.code(str(e))

# ============================================================
# STUDY PLANNER
# ============================================================

elif tool == "📅 Study Planner":

    st.markdown(
        '<div class="section-title">📅 Personal Study Planner</div>',
        unsafe_allow_html=True
    )

    subject = st.text_input(
        "📚 Subject",
        placeholder="Example: Python"
    )

    days = st.number_input(
        "📆 Number of days",
        min_value=1,
        max_value=30,
        value=7
    )

    hours = st.number_input(
        "⏰ Study hours per day",
        min_value=1,
        max_value=12,
        value=2
    )

    if st.button("🚀 Create My Plan", type="primary"):

        if not subject.strip():
            st.warning("⚠️ Enter a subject first.")

        else:

            prompt = f"""
Create a realistic study plan.

Subject: {subject}
Days: {days}
Hours per day: {hours}

Create a day-by-day plan.

Include:
📚 Topics
⏰ Study time
📝 Practice
🔄 Revision
🎯 Goals

Keep it beginner-friendly.
"""

            with st.spinner("📅 Creating your study plan..."):

                try:
                    st.markdown(ask_gemini(prompt))
                except Exception as e:
                    st.error("❌ Could not create study plan.")
                    st.code(str(e))

# ============================================================
# FLASHCARDS
# ============================================================

elif tool == "🧠 Flashcards":

    st.markdown(
        '<div class="section-title">🧠 AI Flashcards</div>',
        unsafe_allow_html=True
    )

    flash_topic = st.text_input(
        "📚 Enter topic",
        placeholder="Example: C++ Basics"
    )

    count = st.slider(
        "🃏 Number of flashcards",
        5,
        20,
        10
    )

    if st.button("🧠 Create Flashcards", type="primary"):

        if not flash_topic.strip():
            st.warning("⚠️ Enter a topic first.")

        else:

            prompt = f"""
Create {count} useful study flashcards about:

{flash_topic}

Format each one as:

### 🃏 Flashcard 1
**Question:** ...
**Answer:** ...

Use simple language.
"""

            with st.spinner("🧠 Creating flashcards..."):

                try:
                    st.markdown(ask_gemini(prompt))
                except Exception as e:
                    st.error("❌ Could not create flashcards.")
                    st.code(str(e))

# ============================================================
# CALCULATOR
# ============================================================

elif tool == "🧮 Calculator":

    st.markdown(
        '<div class="section-title">🧮 Study Calculator</div>',
        unsafe_allow_html=True
    )

    expression = st.text_input(
        "🔢 Enter calculation",
        placeholder="Example: 25 * 4 + 10"
    )

    st.info("⚠️ Use basic mathematical expressions only.")

    if st.button("🧮 Calculate", type="primary"):

        try:

            allowed = "0123456789+-*/(). %"

            if not all(char in allowed for char in expression):
                raise ValueError("Only basic mathematical symbols are allowed.")

            result = eval(expression, {"__builtins__": {}}, {})

            st.success(f"✅ Result: {result}")

        except Exception:
            st.error("❌ Please enter a valid calculation.")

# ============================================================
# TIMER
# ============================================================

elif tool == "⏱️ Study Timer":

    st.markdown(
        '<div class="section-title">⏱️ Focus Study Timer</div>',
        unsafe_allow_html=True
    )

    minutes = st.number_input(
        "⏰ Study duration in minutes",
        min_value=1,
        max_value=120,
        value=25
    )

    if st.button("🚀 Start Timer", type="primary"):

        placeholder = st.empty()

        total_seconds = int(minutes * 60)

        for remaining in range(total_seconds, -1, -1):

            mins = remaining // 60
            secs = remaining % 60

            placeholder.markdown(
                f"""
                <div style="
                    text-align:center;
                    padding:35px;
                    background:white;
                    border-radius:25px;
                    box-shadow:0 10px 30px rgba(0,0,0,0.1);
                ">
                    <div style="font-size:65px;">⏱️</div>
                    <h1 style="color:#071a52;">
                        {mins:02d}:{secs:02d}
                    </h1>
                    <p>📚 Stay focused and keep studying!</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            time.sleep(1)

        st.success("🎉 Time's up! Great work!")

# ============================================================
# STUDY TIPS
# ============================================================

st.markdown(
    '<div class="section-title">🌟 Smart Study Tips</div>',
    unsafe_allow_html=True
)

tip1, tip2, tip3 = st.columns(3)

with tip1:
    st.markdown("""
    <div class="card">
        <div class="card-icon">⏰</div>
        <div class="card-title">Study Regularly</div>
        <div class="card-text">
        Small daily sessions are better than last-minute studying.
        </div>
    </div>
    """, unsafe_allow_html=True)

with tip2:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🧠</div>
        <div class="card-title">Practice More</div>
        <div class="card-text">
        Practice questions regularly to improve your confidence.
        </div>
    </div>
    """, unsafe_allow_html=True)

with tip3:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🔄</div>
        <div class="card-title">Revise</div>
        <div class="card-text">
        Revise important concepts regularly so you remember them longer.
     