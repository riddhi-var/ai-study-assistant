

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
# ========================================= ============================================================
# 🚀 ADVANCED AI DASHBOARD DESIGN
# ============================================================

st.markdown("""
<style>

/* =========================================================
   MAIN BACKGROUND
   ========================================================= */

.stApp {
    background:
        radial-gradient(circle at 10% 20%, rgba(79,70,229,0.22), transparent 25%),
        radial-gradient(circle at 90% 15%, rgba(6,182,212,0.16), transparent 25%),
        radial-gradient(circle at 50% 90%, rgba(124,58,237,0.18), transparent 30%),
        linear-gradient(135deg, #020617 0%, #0f172a 45%, #111827 100%);
    background-attachment: fixed;
}

/* =========================================================
   ANIMATIONS
   ========================================================= */

@keyframes gradientMove {
    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}

@keyframes float {
    0%, 100% {
        transform: translateY(0px);
    }

    50% {
        transform: translateY(-15px);
    }
}

@keyframes pulseGlow {
    0%, 100% {
        box-shadow:
            0 0 10px rgba(99,102,241,0.25),
            0 0 25px rgba(99,102,241,0.10);
    }

    50% {
        box-shadow:
            0 0 25px rgba(129,140,248,0.55),
            0 0 60px rgba(99,102,241,0.25);
    }
}

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(35px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

@keyframes orbRotate {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

@keyframes borderMove {
    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}

/* =========================================================
   HERO
   ========================================================= */

.hero {
    position: relative;
    overflow: hidden;

    padding: 55px 30px;
    margin: 20px 0 35px 0;

    text-align: center;

    border-radius: 30px;

    background:
        linear-gradient(
            135deg,
            rgba(15,23,42,0.95),
            rgba(49,46,129,0.75),
            rgba(30,41,59,0.95)
        );

    background-size: 300% 300%;

    border: 1px solid rgba(129,140,248,0.35);

    animation:
        fadeUp 0.8s ease,
        gradientMove 10s ease infinite;

    box-shadow:
        0 25px 80px rgba(0,0,0,0.35);
}

/* glowing circles behind hero */

.hero::before {
    content: "";
    position: absolute;

    width: 250px;
    height: 250px;

    border-radius: 50%;

    background: rgba(99,102,241,0.12);

    filter: blur(5px);

    top: -100px;
    left: -70px;

    animation: float 5s ease-in-out infinite;
}

.hero::after {
    content: "";

    position: absolute;

    width: 200px;
    height: 200px;

    border-radius: 50%;

    background: rgba(6,182,212,0.10);

    bottom: -90px;
    right: -60px;

    animation: float 6s ease-in-out infinite reverse;
}

/* =========================================================
   HERO ICON
   ========================================================= */

.hero-icon {
    position: relative;
    z-index: 2;

    font-size: 70px;

    display: inline-block;

    animation: float 3s ease-in-out infinite;

    filter:
        drop-shadow(0 0 10px rgba(129,140,248,0.8));
}

/* =========================================================
   HERO TITLE
   ========================================================= */

.hero h1 {
    position: relative;
    z-index: 2;

    font-size: 50px;
    font-weight: 900;

    margin: 10px 0;

    background:
        linear-gradient(
            90deg,
            #a5b4fc,
            #67e8f9,
            #c4b5fd,
            #818cf8
        );

    background-size: 300% auto;

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    animation: gradientMove 6s ease infinite;
}

.hero p {
    position: relative;
    z-index: 2;

    color: #cbd5e1;

    font-size: 18px;
}

/* =========================================================
   SECTION TITLE
   ========================================================= */

.section-title {
    font-size: 30px;
    font-weight: 800;

    margin: 35px 0 20px 0;

    color: #f8fafc;

    animation: fadeUp 0.7s ease;
}

/* =========================================================
   GLASSMORPHISM CARDS
   ========================================================= */

.tool-card {
    position: relative;

    min-height: 190px;

    padding: 25px;

    border-radius: 24px;

    background:
        linear-gradient(
            135deg,
            rgba(30,41,59,0.80),
            rgba(15,23,42,0.65)
        );

    backdrop-filter: blur(18px);

    border: 1px solid rgba(129,140,248,0.22);

    box-shadow:
        0 15px 40px rgba(0,0,0,0.25);

    transition:
        transform 0.35s ease,
        box-shadow 0.35s ease,
        border-color 0.35s ease;

    animation: fadeUp 0.8s ease;

    overflow: hidden;
}

/* animated glow inside card */

.tool-card::before {
    content: "";

    position: absolute;

    width: 120px;
    height: 120px;

    border-radius: 50%;

    background: rgba(99,102,241,0.12);

    filter: blur(20px);

    top: -50px;
    right: -40px;

    transition: 0.4s;
}

.tool-card:hover::before {
    width: 180px;
    height: 180px;
}

/* card hover */

.tool-card:hover {
    transform:
        translateY(-12px)
        scale(1.025);

    border-color:
        rgba(129,140,248,0.75);

    box-shadow:
        0 20px 55px rgba(79,70,229,0.28);
}

/* =========================================================
   CARD ICON
   ========================================================= */

.tool-icon {
    position: relative;

    font-size: 45px;

    display: inline-block;

    animation: float 3s ease-in-out infinite;
}

/* =========================================================
   CARD TEXT
   ========================================================= */

.tool-title {
    font-size: 20px;

    font-weight: 800;

    margin-top: 12px;

    color: #ffffff;
}

.tool-text {
    color: #94a3b8;

    margin-top: 8px;

    line-height: 1.6;
}

/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {

    width: 100%;

    min-height: 48px;

    border-radius: 15px;

    border:
        1px solid rgba(129,140,248,0.40);

    background:
        linear-gradient(
            90deg,
            #312e81,
            #4f46e5,
            #7c3aed,
            #312e81
        );

    background-size: 300% auto;

    color: white;

    font-size: 15px;

    font-weight: 800;

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease,
        background-position 0.5s ease;

    animation: gradientMove 6s ease infinite;
}

.stButton > button:hover {

    transform:
        translateY(-4px)
        scale(1.02);

    background-position:
        100% center;

    box-shadow:
        0 10px 30px rgba(99,102,241,0.55);

    border-color:
        #a5b4fc;
}

.stButton > button:active {

    transform:
        translateY(0)
        scale(0.98);
}

/* =========================================================
   TEXT AREAS
   ========================================================= */

.stTextArea textarea {

    background:
        rgba(15,23,42,0.85) !important;

    color:
        #f8fafc !important;

    border-radius:
        16px !important;

    border:
        1px solid rgba(129,140,248,0.35) !important;

    transition:
        0.3s ease !important;
}

.stTextArea textarea:focus {

    border-color:
        #818cf8 !important;

    box-shadow:
        0 0 20px rgba(99,102,241,0.25) !important;
}

/* =========================================================
   TEXT INPUT
   ========================================================= */

.stTextInput input {

    background:
        rgba(15,23,42,0.85) !important;

    color:
        #ffffff !important;

    border-radius:
        15px !important;

    border:
        1px solid rgba(129,140,248,0.35) !important;
}

/* =========================================================
   SELECT BOX
   ========================================================= */

.stSelectbox > div > div {

    background:
        rgba(15,23,42,0.90) !important;

    border-radius:
        14px !important;

    border:
        1px solid rgba(129,140,248,0.35) !important;
}

/* =========================================================
   ANSWER BOX
   ========================================================= */

.answer-box {

    padding: 25px;

    margin: 25px 0;

    border-radius: 22px;

    background:
        linear-gradient(
            135deg,
            rgba(30,41,59,0.90),
            rgba(49,46,129,0.65)
        );

    backdrop-filter:
        blur(18px);

    border:
        1px solid rgba(129,140,248,0.40);

    animation:
        fadeUp 0.7s ease,
        pulseGlow 3s ease-in-out infinite;
}

/* =========================================================
   AI THINKING EFFECT
   ========================================================= */

.ai-thinking {

    padding: 20px;

    text-align: center;

    border-radius: 20px;

    background:
        rgba(30,41,59,0.75);

    border:
        1px solid rgba(129,140,248,0.30);

    animation:
        pulseGlow 1.5s infinite;
}

/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #020617,
            #0f172a,
            #111827
        );

    border-right:
        1px solid rgba(129,140,248,0.20);
}

.sidebar-title {

    font-size: 25px;

    font-weight: 900;

    color: white;

    padding:
        10px 0 20px 0;
}

.sidebar-card {

    padding: 15px;

    margin: 10px 0;

    border-radius: 16px;

    background:
        rgba(30,41,59,0.65);

    border:
        1px solid rgba(129,140,248,0.20);

    transition:
        0.3s ease;
}

.sidebar-card:hover {

    transform:
        translateX(7px);

    border-color:
        #818cf8;

    box-shadow:
        0 5px 20px rgba(79,70,229,0.20);
}

/* =========================================================
   FOOTER
   ========================================================= */

.footer {

    margin-top: 60px;

    padding: 35px;

    text-align: center;

    border-radius: 25px;

    background:
        linear-gradient(
            135deg,
            rgba(15,23,42,0.85),
            rgba(49,46,129,0.35)
        );

    border:
        1px solid rgba(129,140,248,0.20);

    animation:
        fadeUp 1s ease;
}

.footer h2 {

    color:
        #e0e7ff;

    font-weight:
        900;
}

/* =========================================================
   SCROLLBAR
   ========================================================= */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #020617;
}

::-webkit-scrollbar-thumb {

    background:
        linear-gradient(
            #4f46e5,
            #7c3aed
        );

    border-radius:
        10px;
}

/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 768px) {

    .hero {
        padding: 35px 15px;
    }

    .hero h1 {
        font-size: 34px;
    }

    .hero-icon {
        font-size: 50px;
    }

    .section-title {
        font-size: 24px;
    }
}

</style>
""", unsafe_allow_html=True) ============================================================
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
 