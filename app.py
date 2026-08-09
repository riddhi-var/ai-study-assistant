import streamlit as st
from google import genai
from pypdf import PdfReader

# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# DESIGN / CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 5% 5%, rgba(129,140,248,0.18), transparent 25%),
        radial-gradient(circle at 95% 10%, rgba(34,211,238,0.18), transparent 25%),
        radial-gradient(circle at 50% 100%, rgba(244,114,182,0.12), transparent 30%),
        #f8fafc;
}

.main .block-container {
    max-width: 1250px;
    padding-top: 25px;
    padding-bottom: 60px;
}

/* TOP NAVBAR */

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 17px 24px;
    background: rgba(255,255,255,0.95);
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(15,23,42,0.08);
    margin-bottom: 30px;
}

.logo-area {
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo-icon {
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 15px;
    background: linear-gradient(135deg,#4f46e5,#7c3aed);
    font-size: 27px;
    box-shadow: 0 8px 20px rgba(79,70,229,0.25);
}

.logo-title {
    font-size: 23px;
    font-weight: 900;
    color: #172554;
}

.logo-title span {
    color: #6366f1;
}

.logo-subtitle {
    color: #64748b;
    font-size: 12px;
}

.student-badge {
    background: #eef2ff;
    color: #3730a3;
    padding: 10px 17px;
    border-radius: 30px;
    font-size: 14px;
    font-weight: 700;
}

/* HERO */

.hero {
    min-height: 320px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 45px;
    border-radius: 30px;
    background: linear-gradient(135deg,#312e81,#4f46e5 50%,#0891b2);
    overflow: hidden;
    position: relative;
    box-shadow: 0 20px 45px rgba(49,46,129,0.25);
    margin-bottom: 35px;
}

.hero::before {
    content: "";
    position: absolute;
    width: 250px;
    height: 250px;
    border-radius: 50%;
    background: rgba(255,255,255,0.10);
    right: 120px;
    top: -100px;
}

.hero::after {
    content: "";
    position: absolute;
    width: 180px;
    height: 180px;
    border-radius: 50%;
    background: rgba(255,255,255,0.08);
    right: -50px;
    bottom: -70px;
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 700px;
}

.hero-small {
    color: #c7d2fe;
    font-size: 14px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero-title {
    color: white;
    font-size: 45px;
    line-height: 1.15;
    font-weight: 900;
    margin: 0;
}

.hero-title span {
    color: #67e8f9;
}

.hero-description {
    color: #e0e7ff;
    font-size: 17px;
    line-height: 1.6;
    margin-top: 15px;
}

.hero-pills {
    display: flex;
    gap: 10px;
    margin-top: 22px;
    flex-wrap: wrap;
}

.hero-pill {
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.20);
    color: white;
    padding: 8px 13px;
    border-radius: 30px;
    font-size: 13px;
}

/* STUDENT IMAGE / ICON */

.student-art {
    position: relative;
    width: 260px;
    height: 240px;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2;
}

.student-circle {
    width: 210px;
    height: 210px;
    border-radius: 50%;
    background: linear-gradient(135deg,#ffffff,#e0f2fe);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 105px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.20);
    animation: floating 3s ease-in-out infinite;
}

.book-float {
    position: absolute;
    left: 10px;
    bottom: 20px;
    font-size: 45px;
    animation: floating 2.5s ease-in-out infinite;
}

.ai-float {
    position: absolute;
    right: 5px;
    top: 15px;
    font-size: 45px;
    animation: floating 2s ease-in-out infinite;
}

@keyframes floating {
    0%,100% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(-12px);
    }
}

/* SECTION */

.section-title {
    text-align: center;
    color: #172554;
    font-size: 29px;
    font-weight: 900;
    margin-top: 25px;
    margin-bottom: 7px;
}

.section-subtitle {
    text-align: center;
    color: #64748b;
    margin-bottom: 25px;
}

/* CARDS */

.feature-card {
    min-height: 200px;
    padding: 25px;
    border-radius: 23px;
    margin-bottom: 18px;
    border: 1px solid rgba(255,255,255,0.9);
    box-shadow: 0 10px 28px rgba(15,23,42,0.08);
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}

.feature-card:hover {
    transform: translateY(-7px);
    box-shadow: 0 20px 38px rgba(15,23,42,0.15);
}

.feature-card::after {
    content: "";
    position: absolute;
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: rgba(255,255,255,0.25);
    right: -35px;
    bottom: -35px;
}

.blue {
    background: linear-gradient(135deg,#dbeafe,#bfdbfe);
}

.purple {
    background: linear-gradient(135deg,#ede9fe,#ddd6fe);
}

.orange {
    background: linear-gradient(135deg,#ffedd5,#fed7aa);
}

.cyan {
    background: linear-gradient(135deg,#cffafe,#a5f3fc);
}

.pink {
    background: linear-gradient(135deg,#fce7f3,#fbcfe8);
}

.green {
    background: linear-gradient(135deg,#dcfce7,#bbf7d0);
}

.feature-icon {
    font-size: 42px;
    margin-bottom: 10px;
}

.feature-title {
    color: #172554;
    font-size: 20px;
    font-weight: 900;
}

.feature-description {
    color: #475569;
    font-size: 14px;
    line-height: 1.5;
    margin-top: 8px;
}

/* BUTTONS */

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg,#4f46e5,#7c3aed);
    color: white !important;
    border: none;
    border-radius: 12px;
    font-weight: 800;
    padding: 10px 18px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(79,70,229,0.25);
}

/* AI SECTION */

.ai-box {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 27px;
    padding: 30px;
    margin-top: 30px;
    box-shadow: 0 12px 35px rgba(15,23,42,0.09);
}

.ai-heading {
    color: #312e81;
    font-size: 28px;
    font-weight: 900;
    text-align: center;
}

.ai-subheading {
    color: #64748b;
    text-align: center;
    margin-bottom: 22px;
}

/* TEXT AREA */

.stTextArea textarea {
    background: #f8fafc !important;
    color: #172554 !important;
    border: 2px solid #c7d2fe !important;
    border-radius: 15px !important;
    font-size: 16px !important;
}

.stTextArea textarea:focus {
    border: 2px solid #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}

/* ANSWER */

.answer-box {
    background: white;
    border-radius: 20px;
    padding: 25px;
    margin-top: 25px;
    border-left: 6px solid #6366f1;
    box-shadow: 0 10px 30px rgba(15,23,42,0.08);
}

/* FOOTER */

.footer {
    text-align: center;
    margin-top: 55px;
    padding-top: 25px;
    border-top: 1px solid #e2e8f0;
    color: #64748b;
    line-height: 1.8;
}

.footer-title {
    color: #312e81;
    font-size: 18px;
    font-weight: 900;
}

/* MOBILE */

@media (max-width:800px) {

    .hero {
        padding: 30px;
    }

    .hero-title {
        font-size: 32px;
    }

    .student-art {
        display: none;
    }

    .student-badge {
        display: none;
    }
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# GEMINI CONNECTION
# ============================================================

if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ Gemini API key is missing.")
    st.info("Open Streamlit → Manage app → Settings → Secrets and add GEMINI_API_KEY.")
    st.stop()

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# ============================================================
# NAVBAR
# ============================================================

st.markdown("""
<div class="navbar">
    <div class="logo-area">
        <div class="logo-icon">📚</div>
        <div>
            <div class="logo-title">AI Study <span>Assistant</span></div>
            <div class="logo-subtitle">Your smart learning companion 🤖</div>
        </div>
    </div>
    <div class="student-badge">🎓 Student Mode</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">
    <div class="hero-content">
        <div class="hero-small">✨ WELCOME TO YOUR AI STUDY SPACE</div>
        <h1 class="hero-title">
            Learn smarter.<br>
            Study <span>better.</span> 🚀
        </h1>
        <div class="hero-description">
            Your personal AI tutor for understanding difficult topics,
            preparing quizzes, summarizing notes and planning your studies.
        </div>
        <div class="hero-pills">
            <div class="hero-pill">🤖 AI Tutor</div>
            <div class="hero-pill">📚 Smart Learning</div>
            <div class="hero-pill">🎯 Practice</div>
            <div class="hero-pill">🏆 Improve</div>
        </div>
    </div>
    <div class="student-art">
        <div class="student-circle">🧑‍🎓</div>
        <div class="book-float">📚</div>
        <div class="ai-float">🤖</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TOOLKIT
# ============================================================

st.markdown("""
<div class="section-title">🎓 Your Study Toolkit</div>
<div class="section-subtitle">
    Everything you need to study smarter in one place.
</div>
""", unsafe_allow_html=True)

# ============================================================
# CARD ROW 1
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card blue">
        <div class="feature-icon">💬</div>
        <div class="feature-title">Ask AI</div>
        <div class="feature-description">
            Ask any study question and receive a simple,
            beginner-friendly explanation.
        </div>
    </div>
    """, unsafe_allow_html=True)
    ask_button = st.button("💬 Ask AI", key="ask_ai_button")

with col2:
    st.markdown("""
    <div class="feature-card purple">
        <div class="feature-icon">📖</div>
        <div class="feature-title">Explain Topic</div>
        <div class="feature-description">
            Understand difficult concepts using examples
            and simple language.
        </div>
    </div>
    """, unsafe_allow_html=True)
    explain_button = st.button("📖 Explain Topic", key="explain_button")

with col3:
    st.markdown("""
    <div class="feature-card orange">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">Quiz Generator</div>
        <div class="feature-description">
            Generate practice questions and test
            your knowledge.
        </div>
    </div>
    """, unsafe_allow_html=True)
    quiz_button = st.button("🎯 Generate Quiz", key="quiz_button")

# ============================================================
# CARD ROW 2
# ============================================================

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="feature-card cyan">
        <div class="feature-icon">📄</div>
        <div class="feature-title">PDF Study</div>
        <div class="feature-description">
            Upload your notes or textbook PDF and
            ask questions from it.
        </div>
    </div>
    """, unsafe_allow_html=True)
    pdf_button = st.button("📄 Study PDF", key="pdf_button")

with col5:
    st.markdown("""
    <div class="feature-card pink">
        <div class="feature-icon">📝</div>
        <div class="feature-title">Smart Notes</div>
        <div class="feature-description">
            Convert long notes into short and useful
            revision points.
        </div>
    </div>
    """, unsafe_allow_html=True)
    notes_button = st.button("📝 Summarize Notes", key="notes_button")

with col6:
    st.markdown("""
    <div class="feature-card green">
        <div class="feature-icon">📅</div>
        <div class="feature-title">Study Planner</div>
        <div class="feature-description">
            Create a personalized daily or weekly
            study schedule.
        </div>
    </div>
    """, unsafe_allow_html=True)
    planner_button = st.button("📅 Make Study Plan", key="planner_button")

# ============================================================
# AI ASSISTANT
# ============================================================

st.markdown("""
<div class="ai-box">
    <div class="ai-heading">✨ Ask Your AI Tutor</div>
    <div class="ai-subheading">
        Ask anything about your studies and get a simple explanation.
    </div>
</div>
""", unsafe_allow_html=True)

question = st.text_area(
    "💭 Your Question",
    placeholder="Example: Explain Python variables in very simple language...",
    height=140
)

# ============================================================
# GEMINI FUNCTION
# ============================================================

def ask_gemini(prompt):

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=f"""
You are a friendly AI Study Assistant.

Help the student understand the following question
in very simple and beginner-friendly language.

Use examples whenever useful.

Student question:
{prompt}

Format the answer as:

## 📖 Simple Explanation

## 💡 Example

## ⭐ Important Points

## 📝 Short Summary

Avoid unnecessarily complicated words.
"""
    )

    return response.text

# ============================================================
# ASK AI
# ============================================================

if st.button("🤖 Ask AI", key="main_question_button"):

    if not question.strip():

        st.warning("⚠️ Please enter your question first.")

    else:

        with st.spinner("🤖 Your AI tutor is thinking..."):

            try:

                answer = ask_gemini(question)

                st.markdown("""
                <div class="answer-box">
                    <h3 style="color:#312e81;">
                        🤖 AI Tutor Answer
                    </h3>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(answer)

            except Exception as e:

                st.error("❌ Gemini could not answer right now.")
                st.code(str(e))

# ============================================================
# EXPLAIN TOPIC
# ============================================================

if explain_button:

    st.info(
        "📖 Type your topic in the question box above. "
        "Example: Explain recursion in Python."
    )

# ============================================================
# QUIZ
# ============================================================

if quiz_button:

    quiz_topic = st.text_input(
        "🎯 Enter topic for quiz",
        placeholder="Example: Python Basics"
    )

    if st.button("🚀 Create Quiz", key="create_quiz"):

        if quiz_topic.strip():

            with st.spinner("🎯 Creating your quiz..."):

                try:

                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=f"""
Create a 10-question multiple-choice quiz.

Topic: {quiz_topic}

For every question give:

1. Question
A.
B.
C.
D.

Then provide the correct answer.

Keep the difficulty beginner-friendly.
"""
                    )

                    st.markdown(response.text)

                except Exception as e:

                    st.error("❌ Could not generate quiz.")
                    st.code(str(e))

# ============================================================
# PDF STUDY
# ============================================================

if pdf_button:

    st.markdown("### 📄 Upload Your Study PDF")

    uploaded_pdf = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        key="study_pdf"
    )

    if uploaded_pdf:

        reader = PdfReader(uploaded_pdf)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        st.success(
            f"✅ PDF loaded successfully! "
            f"{len(reader.pages)} page(s) found."
        )

        pdf_question = st.text_area(
            "💭 Ask something about your PDF",
            placeholder="What is the main topic of this PDF?",
            key="pdf_question"
        )

        if st.button("🤖 Ask PDF", key="ask_pdf"):

            if pdf_question.strip():

                with st.spinner("📚 Reading your PDF..."):

                    try:

                        response = client.models.generate_content(
                            model="gemini-3.5-flash-lite",
                            contents=f"""
You are a study assistant.

Answer the student's question using
the following PDF content.

PDF content:
{text[:30000]}

Student question:
{pdf_question}

Answer in simple language.
"""
                        )

                        st.markdown(response.text)

                    except Exception as e:

                        st.error("❌ Could not process the PDF.")
                        st.code(str(e))

# ============================================================
# NOTES
# ============================================================

if notes_button:

    notes = st.text_area(
        "📝 Paste your notes here",
        height=200,
        placeholder="Paste your study notes...",
        key="notes_input"
    )

    if st.button("✨ Summarize Notes", key="summarize_notes"):

        if notes.strip():

            with st.spinner("📝 Creating your summary..."):

                try:

                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=f"""
Summarize these study notes.

Notes:
{notes}

Give:

📌 Key Concepts
⭐ Important Points
📝 Short Revision Notes
❓ Possible Exam Questions

Use very simple language.
"""
                    )

                    st.markdown(response.text)

                except Exception as e:

                    st.error("❌ Could not summarize notes.")
                    st.code(str(e))

# ============================================================
# STUDY PLANNER
# ============================================================

if planner_button:

    st.markdown("### 📅 Create Your Study Plan")

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

    if st.button("🚀 Create My Plan", key="create_plan"):

        if subject.strip():

            with st.spinner("📅 Creating your study plan..."):

                try:

                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=f"""
Create a study plan for a student.

Subject: {subject}
Number of days: {days}
Study hours per day: {hours}

Create a day-by-day plan.

Include:
📚 Topics
⏰ Suggested study time
📝 Practice
🔄 Revision

Keep it realistic and beginner-friendly.
"""
                    )

                    st.markdown(response.text)

                except Exception as e:

                    st.error("❌ Could not create study plan.")
                    st.code(str(e))

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

    <div class="footer-title">
        📚 AI Study Assistant
    </div>

    Your personal AI tutor 🤖

    <br><br>

    🐍 Python &nbsp; • &nbsp;
    🎈 Streamlit &nbsp; • &nbsp;
    ✨ Gemini AI

    <br>

    💬 Learn &nbsp; • &nbsp;
    📖 Practice &nbsp; • &nbsp;
    🎯 Revise &nbsp; • &nbsp;
    🏆 Succeed

</div>
""", unsafe_allow_html=True)
