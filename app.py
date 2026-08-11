

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

css = """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(79,70,229,0.20), transparent 30%),
        radial-gradient(circle at 90% 10%, rgba(14,165,233,0.15), transparent 30%),
        linear-gradient(135deg, #020617 0%, #0f172a 45%, #111827 100%);
    color: #f8fafc;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #111827);
    border-right: 1px solid rgba(148,163,184,0.20);
}

.sidebar-title {
    font-size: 25px;
    font-weight: 800;
    color: #ffffff;
    padding: 10px 0 20px 0;
}

.sidebar-card {
    padding: 14px;
    margin: 10px 0;
    border-radius: 15px;
    background: rgba(30,41,59,0.70);
    border: 1px solid rgba(99,102,241,0.25);
    transition: 0.3s;
}

.sidebar-card:hover {
    transform: translateX(5px);
    border-color: #818cf8;
}

/* Hero */

.hero {
    padding: 50px 30px;
    border-radius: 30px;
    text-align: center;
    background:
        linear-gradient(135deg, rgba(30,41,59,0.95), rgba(49,46,129,0.75));
    border: 1px solid rgba(129,140,248,0.30);
    box-shadow: 0 20px 60px rgba(0,0,0,0.30);
    animation: fadeUp 0.8s ease;
    margin-bottom: 30px;
}

.hero-icon {
    font-size: 65px;
    animation: floatIcon 3s ease-in-out infinite;
}

.hero h1 {
    font-size: 48px;
    font-weight: 800;
    margin: 10px 0;
    background: linear-gradient(90deg, #a5b4fc, #67e8f9, #c4b5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    font-size: 19px;
    color: #cbd5e1;
}

/* Section */

.section-title {
    font-size: 30px;
    font-weight: 800;
    margin: 30px 0 18px 0;
    color: #f8fafc;
}

/* Cards */

.tool-card {
    min-height: 190px;
    padding: 25px;
    border-radius: 22px;
    background: rgba(15,23,42,0.80);
    border: 1px solid rgba(129,140,248,0.22);
    box-shadow: 0 12px 35px rgba(0,0,0,0.20);
    transition: all 0.3s ease;
    animation: fadeUp 0.7s ease;
}

.tool-card:hover {
    transform: translateY(-8px);
    border-color: #818cf8;
    box-shadow: 0 20px 50px rgba(79,70,229,0.25);
}

.tool-icon {
    font-size: 42px;
}

.tool-title {
    font-size: 20px;
    font-weight: 800;
    margin-top: 10px;
    color: #ffffff;
}

.tool-text {
    color: #94a3b8;
    margin-top: 8px;
}

/* Buttons */

.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: 1px solid rgba(129,140,248,0.40);
    background: linear-gradient(135deg, #312e81, #4f46e5);
    color: white;
    font-weight: 700;
    padding: 12px;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(79,70,229,0.40);
    border-color: #a5b4fc;
}

/* Text input */

.stTextArea textarea,
.stTextInput input,
.stNumberInput input {
    background: rgba(15,23,42,0.85) !important;
    color: white !important;
    border-radius: 14px !important;
    border: 1px solid rgba(129,140,248,0.35) !important;
}

/* Answer */

.answer-box {
    padding: 22px;
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(30,41,59,0.95), rgba(49,46,129,0.55));
    border: 1px solid rgba(129,140,248,0.35);
    margin: 20px 0;
    animation: fadeUp 0.6s ease;
}

/* Footer */

.footer {
    margin-top: 60px;
    padding: 30px;
    text-align: center;
    border-radius: 22px;
    background: rgba(15,23,42,0.75);
    border: 1px solid rgba(129,140,248,0.20);
    color: #94a3b8;
}

/* Animations */

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes floatIcon {
    0%,100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-12px);
    }
}

</style>
"""

st.markdown(css, unsafe_allow_html=True)

# ============================================================
# GEMINI CONNECTION
# ============================================================

if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔐 Gemini API key is missing.")
    st.info("Go to Streamlit → Manage app → Settings → Secrets.")
    st.code('GEMINI_API_KEY = "your-api-key-here"')
    st.stop()

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

MODEL = "gemini-2.5-flash"

# ============================================================
# HELPER FUNCTION
# ============================================================

def ask_gemini(prompt):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🎓 Study Center</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-card">💬 <b>Ask AI</b><br><small>Ask any study question.</small></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-card">📄 <b>PDF Study</b><br><small>Ask questions from your PDF.</small></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-card">📝 <b>Smart Notes</b><br><small>Summarize long notes.</small></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-card">🎯 <b>Quiz Generator</b><br><small>Practice your knowledge.</small></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-card">🧠 <b>Flashcards</b><br><small>Remember concepts faster.</small></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-card">📅 <b>Study Planner</b><br><small>Create your study routine.</small></div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### 🌟 Features")

    st.markdown(
        "📚 Simple explanations\n\n"
        "🤖 AI-powered learning\n\n"
        "📄 PDF study assistant\n\n"
        "🎯 Quiz practice\n\n"
        "🧠 Flashcards\n\n"
        "⏱️ Focus timer"
    )

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-icon">📚</div>
        <h1>AI Study Assistant</h1>
        <p>Your personal AI tutor 🤖</p>
        <p>Learn • Practice • Revise • Succeed ✨</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# TOOL SELECTION
# ============================================================

st.markdown(
    '<div class="section-title">🚀 Choose Your Study Tool</div>',
    unsafe_allow_html=True
)

tool1, tool2, tool3, tool4 = st.columns(4)

with tool1:
    st.markdown(
        """
        <div class="tool-card">
            <div class="tool-icon">💬</div>
            <div class="tool-title">Ask AI</div>
            <div class="tool-text">Ask anything about your studies.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with tool2:
    st.markdown(
        """
        <div class="tool-card">
            <div class="tool-icon">📄</div>
            <div class="tool-title">Study PDF</div>
            <div class="tool-text">Upload notes and ask questions.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with tool3:
    st.markdown(
        """
        <div class="tool-card">
            <div class="tool-icon">🎯</div>
            <div class="tool-title">Quiz</div>
            <div class="tool-text">Create quizzes for practice.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with tool4:
    st.markdown(
        """
        <div class="tool-card">
            <div class="tool-icon">🧠</div>
            <div class="tool-title">Flashcards</div>
            <div class="tool-text">Learn using quick revision cards.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# BUTTON NAVIGATION
# ============================================================

st.markdown("### 🎮 Open a Tool")

b1, b2, b3, b4, b5, b6 = st.columns(6)

with b1:
    ask_mode = st.button("💬 Ask AI")

with b2:
    pdf_mode = st.button("📄 PDF")

with b3:
    quiz_mode = st.button("🎯 Quiz")

with b4:
    notes_mode = st.button("📝 Notes")

with b5:
    flash_mode = st.button("🧠 Flashcards")

with b6:
    plan_mode = st.button("📅 Planner")

if ask_mode:
    st.session_state["tool"] = "ask"

if pdf_mode:
    st.session_state["tool"] = "pdf"

if quiz_mode:
    st.session_state["tool"] = "quiz"

if notes_mode:
    st.session_state["tool"] = "notes"

if flash_mode:
    st.session_state["tool"] = "flash"

if plan_mode:
    st.session_state["tool"] = "plan"

if "tool" not in st.session_state:
    st.session_state["tool"] = "ask"

# ============================================================
# ASK AI
# ============================================================

if st.session_state["tool"] == "ask":

    st.markdown(
        '<div class="section-title">🤖 Ask Your AI Tutor</div>',
        unsafe_allow_html=True
    )

    question = st.text_area(
        "💭 Your Question",
        placeholder="Example: Explain Python variables in very simple language...",
        height=150
    )

    if st.button("🚀 Ask AI Tutor", key="ask_main"):

        if not question.strip():
            st.warning("⚠️ Please enter your question first.")

        else:

            prompt = (
                "You are a friendly AI Study Assistant.\n\n"
                "Student question:\n"
                + question
                + "\n\n"
                "Explain in very simple beginner-friendly language.\n\n"
                "Use this structure:\n"
                "## 📖 Simple Explanation\n"
                "## 💡 Example\n"
                "## 📝 Important Points\n"
                "## 🎯 Quick Revision\n"
                "## ❓ One Practice Question\n"
            )

            with st.spinner("🤖 AI tutor is thinking..."):

                try:
                    answer = ask_gemini(prompt)

                    st.markdown(
                        '<div class="answer-box"><h2>📖 AI Tutor Answer</h2></div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(answer)
                    st.success("✅ Answer generated! Keep learning 🚀")

                except Exception as e:
                    st.error("❌ Gemini could not answer right now.")
                    st.code(str(e))

# ============================================================
# PDF STUDY
# ============================================================

elif st.session_state["tool"] == "pdf":

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

            pdf_text = ""

            for page in reader.pages:
                extracted = page.extract_text()

                if extracted:
                    pdf_text += extracted + "\n"

            st.success(
                "✅ PDF loaded successfully! "
                + str(len(reader.pages))
                + " page(s) found."
            )

            pdf_question = st.text_area(
                "💭 Ask a question about your PDF",
                placeholder="Example: What are the main points?"
            )

            if st.button("📚 Ask From PDF"):

                if not pdf_question.strip():
                    st.warning("⚠️ Please enter a question.")

                else:

                    prompt = (
                        "You are a study assistant.\n\n"
                        "Use the following PDF content to answer the question.\n\n"
                        "PDF content:\n"
                        + pdf_text[:30000]
                        + "\n\nStudent question:\n"
                        + pdf_question
                        + "\n\nAnswer in simple language."
                    )

                    with st.spinner("📖 Reading your PDF..."):

                        try:
                            answer = ask_gemini(prompt)
                            st.markdown(
                                '<div class="answer-box"><h2>📚 PDF Answer</h2></div>',
                                unsafe_allow_html=True
                            )
                            st.markdown(answer)

                        except Exception as e:
                            st.error("❌ Could not process the PDF.")
                            st.code(str(e))

        except Exception as e:
            st.error("❌ Could not read this PDF.")
            st.code(str(e))

# ============================================================
# QUIZ
# ============================================================

elif st.session_state["tool"] == "quiz":

    st.markdown(
        '<div class="section-title">🎯 AI Quiz Generator</div>',
        unsafe_allow_html=True
    )

    quiz_topic = st.text_input(
        "📚 Quiz Topic",
        placeholder="Example: Python Basics"
    )

    quiz_level = st.selectbox(
        "📊 Difficulty",
        ["Beginner", "Intermediate", "Advanced"]
    )

    if st.button("🎯 Generate Quiz"):

        if not quiz_topic.strip():
            st.warning("⚠️ Enter a topic first.")

        else:

            prompt = (
                "Create a 10-question multiple-choice quiz.\n\n"
                "Topic: "
                + quiz_topic
                + "\n"
                "Difficulty: "
                + quiz_level
                + "\n\n"
                "For every question provide options A, B, C and D.\n"
                "After all questions, provide an answer key.\n"
                "Keep it educational and clear."
            )

            with st.spinner("🎯 Creating your quiz..."):

                try:
                    answer = ask_gemini(prompt)

                    st.markdown(
                        '<div class="answer-box"><h2>🎯 Your Quiz</h2></div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(answer)

                except Exception as e:
                    st.error("❌ Quiz generation failed.")
                    st.code(str(e))

# ============================================================
# NOTES
# ============================================================

elif st.session_state["tool"] == "notes":

    st.markdown(
        '<div class="section-title">📝 Smart Notes Summarizer</div>',
        unsafe_allow_html=True
    )

    notes = st.text_area(
        "📖 Paste your study notes",
        height=250,
        placeholder="Paste your long study notes here..."
    )

    if st.button("✨ Summarize Notes"):

        if not notes.strip():
            st.warning("⚠️ Please paste your notes.")

        else:

            prompt = (
                "Summarize the following study notes in simple language.\n\n"
                "Notes:\n"
                + notes
                + "\n\n"
                "Use this structure:\n"
                "## 📌 Key Concepts\n"
                "## ⭐ Important Points\n"
                "## 📝 Revision Notes\n"
                "## ❓ Possible Exam Questions\n"
            )

            with st.spinner("📝 Creating your summary..."):

                try:
                    answer = ask_gemini(prompt)

                    st.markdown(
                        '<div class="answer-box"><h2>📝 Smart Summary</h2></div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(answer)

                except Exception as e:
                    st.error("❌ Could not summarize notes.")
                    st.code(str(e))

# ============================================================
# FLASHCARDS
# ============================================================

elif st.session_state["tool"] == "flash":

    st.markdown(
        '<div class="section-title">🧠 AI Flashcard Generator</div>',
        unsafe_allow_html=True
    )

    flash_topic = st.text_input(
        "📚 Flashcard Topic",
        placeholder="Example: C++ OOP"
    )

    if st.button("🧠 Create Flashcards"):

        if not flash_topic.strip():
            st.warning("⚠️ Enter a topic first.")

        else:

            prompt = (
                "Create 10 useful study flashcards for the topic: "
                + flash_topic
                + "\n\n"
                "Format each one as:\n"
                "### 🟦 Card 1\n"
                "**Question:** ...\n"
                "**Answer:** ...\n\n"
                "Use simple language."
            )

            with st.spinner("🧠 Creating flashcards..."):

                try:
                    answer = ask_gemini(prompt)

                    st.markdown(
                        '<div class="answer-box"><h2>🧠 Flashcards</h2></div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(answer)

                except Exception as e:
                    st.error("❌ Could not create flashcards.")
                    st.code(str(e))

# ============================================================
# STUDY PLANNER
# ============================================================

elif st.session_state["tool"] == "plan":

    st.markdown(
        '<div class="section-title">📅 Smart Study Planner</div>',
        unsafe_allow_html=True
    )

    subject = st.text_input(
        "📚 Subject",
        placeholder="Example: Python"
    )

    days = st.number_input(
        "📆 Number of Days",
        min_value=1,
        max_value=30,
        value=7
    )

    hours = st.number_input(
        "⏰ Study Hours Per Day",
        min_value=1,
        max_value=12,
        value=2
    )

    if st.button("🚀 Create Study Plan"):

        if not subject.strip():
            st.warning("⚠️ Enter a subject first.")

        else:

            prompt = (
                "Create a realistic study plan.\n\n"
                "Subject: "
                + subject
                + "\n"
                "Days: "
                + str(days)
                + "\n"
                "Study hours per day: "
                + str(hours)
                + "\n\n"
                "Create a day-by-day plan.\n"
                "Include topics, study time, practice and revision.\n"
                "Keep it beginner-friendly."
            )

            with st.spinner("📅 Creating your study plan..."):

                try:
                    answer = ask_gemini(prompt)

                    st.markdown(
                        '<div class="answer-box"><h2>📅 Your Study Plan</h2></div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(answer)

                except Exception as e:
                    st.error("❌ Could not create study plan.")
                    st.code(str(e))

# ============================================================
# POMODORO TIMER
# =============
 