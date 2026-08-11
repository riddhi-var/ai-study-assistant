import streamlit as st
from google import genai
from pypdf import PdfReader
from datetime import date

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="StudyAI - AI Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ANIMATED NAVY BLUE DESIGN
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(59,130,246,.16), transparent 25%),
        radial-gradient(circle at 90% 20%, rgba(99,102,241,.13), transparent 25%),
        linear-gradient(135deg, #020617 0%, #0f172a 48%, #172554 100%);
    color: #f8fafc;
}

.main .block-container {
    padding-top: 2rem;
    max-width: 1400px;
}

/* ---------- ANIMATIONS ---------- */

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(25px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes floating {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-9px);
    }
}

@keyframes glow {
    0%, 100% {
        box-shadow: 0 0 10px rgba(59,130,246,.15);
    }
    50% {
        box-shadow: 0 0 30px rgba(59,130,246,.45);
    }
}

@keyframes pulse {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: .55;
    }
}

/* ---------- HERO ---------- */

.hero {
    padding: 42px 30px;
    border-radius: 28px;
    text-align: center;
    background:
        linear-gradient(135deg,
        rgba(30,64,175,.82),
        rgba(30,27,75,.9));
    border: 1px solid rgba(147,197,253,.22);
    animation: fadeUp .8s ease;
    box-shadow: 0 20px 60px rgba(0,0,0,.28);
    margin-bottom: 25px;
}

.hero-icon {
    font-size: 58px;
    animation: floating 3s ease-in-out infinite;
}

.hero h1 {
    font-size: 48px;
    margin: 5px 0;
    font-weight: 800;
    color: white;
}

.hero p {
    color: #dbeafe;
    font-size: 19px;
}

/* ---------- STAT CARDS ---------- */

.stat-card {
    background: rgba(15,23,42,.72);
    border: 1px solid rgba(148,163,184,.18);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    animation: fadeUp .8s ease;
    transition: .3s;
}

.stat-card:hover {
    transform: translateY(-6px);
    border-color: rgba(96,165,250,.5);
}

.stat-number {
    font-size: 30px;
    font-weight: 800;
    color: #93c5fd;
}

.stat-label {
    color: #94a3b8;
}

/* ---------- TOOL CARDS ---------- */

.tool-card {
    padding: 24px;
    min-height: 170px;
    border-radius: 22px;
    background: linear-gradient(
        145deg,
        rgba(30,41,59,.95),
        rgba(15,23,42,.9)
    );
    border: 1px solid rgba(148,163,184,.17);
    transition: all .35s ease;
    animation: fadeUp .9s ease;
    margin-bottom: 15px;
}

.tool-card:hover {
    transform: translateY(-9px) scale(1.015);
    border-color: rgba(96,165,250,.55);
    animation: glow 2s infinite;
}

.tool-icon {
    font-size: 42px;
    animation: floating 4s ease-in-out infinite;
}

.tool-card h3 {
    color: #f8fafc;
}

.tool-card p {
    color: #94a3b8;
}

/* ---------- SECTION ---------- */

.section-title {
    color: #e0f2fe;
    font-size: 28px;
    font-weight: 800;
    margin-top: 28px;
    margin-bottom: 18px;
    animation: fadeUp .7s ease;
}

/* ---------- AI PANEL ---------- */

.ai-panel {
    padding: 30px;
    border-radius: 25px;
    background:
        linear-gradient(
            135deg,
            rgba(30,64,175,.28),
            rgba(15,23,42,.92)
        );
    border: 1px solid rgba(96,165,250,.3);
    animation: fadeUp .8s ease;
    margin-top: 20px;
}

/* ---------- ACHIEVEMENT ---------- */

.achievement {
    background: rgba(15,23,42,.8);
    border: 1px solid rgba(251,191,36,.25);
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    transition: .3s;
}

.achievement:hover {
    transform: scale(1.04);
}

/* ---------- TIP ---------- */

.tip {
    padding: 22px;
    border-radius: 20px;
    background: linear-gradient(
        135deg,
        rgba(30,64,175,.35),
        rgba(79,70,229,.25)
    );
    border: 1px solid rgba(147,197,253,.2);
    animation: glow 3s infinite;
}

/* ---------- FOOTER ---------- */

.footer {
    text-align: center;
    color: #64748b;
    padding: 35px;
}

/* ---------- STREAMLIT BUTTONS ---------- */

.stButton > button {
    width: 100%;
    border-radius: 13px;
    border: 1px solid rgba(96,165,250,.35);
    background: linear-gradient(135deg,#2563eb,#4338ca);
    color: white;
    font-weight: 700;
    transition: all .25s ease;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(37,99,235,.35);
    border-color: #93c5fd;
}

/* ---------- INPUTS ---------- */

textarea, input {
    border-radius: 12px !important;
}

/* ---------- SIDEBAR ---------- */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#020617,#0f172a);
    border-right: 1px solid rgba(96,165,250,.15);
}

.sidebar-title {
    font-size: 24px;
    font-weight: 800;
    color: #bfdbfe;
    margin-bottom: 20px;
}

/* ---------- PROGRESS ---------- */

.progress-box {
    background: rgba(15,23,42,.8);
    padding: 20px;
    border-radius: 20px;
    border: 1px solid rgba(96,165,250,.2);
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================

if "xp" not in st.session_state:
    st.session_state.xp = 120

if "questions" not in st.session_state:
    st.session_state.questions = 0

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 86

if "streak" not in st.session_state:
    st.session_state.streak = 7

# ============================================================
# GEMINI
# ============================================================

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    client = None

def ask_gemini(prompt):
    if client is None:
        return "🔐 Gemini API key is missing. Add GEMINI_API_KEY in Streamlit Secrets."

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">📚 StudyAI</div>',
        unsafe_allow_html=True
    )

    st.caption("Your intelligent learning companion 🤖")

    page = st.radio(
        "🚀 Study Center",
        [
            "🏠 Dashboard",
            "💬 AI Tutor",
            "📖 Explain Topic",
            "📝 Smart Notes",
            "🎯 Quiz Arena",
            "🧠 Flashcards",
            "📄 PDF Brain",
            "📅 Study Planner",
            "⏱️ Focus Mode"
        ]
    )

    st.markdown("---")

    st.markdown("### 🔥 Your Progress")

    st.metric("🔥 Streak", f"{st.session_state.streak} days")

    st.metric("⭐ XP", st.session_state.xp)

    st.markdown("---")

    st.caption("🐍 Python")
    st.caption("🎈 Streamlit")
    st.caption("🤖 Gemini AI")

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">

<div class="hero-icon">📚</div>

<h1>StudyAI</h1>

<p>Your personal AI-powered study companion 🤖</p>

<p>
✨ Learn &nbsp; • &nbsp;
🧠 Practice &nbsp; • &nbsp;
🎯 Improve &nbsp; • &nbsp;
🏆 Succeed
</p>

</div>
""", unsafe_allow_html=True)

# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="section-title">👋 Welcome back, Student!</div>',
        unsafe_allow_html=True
    )

    st.write("Ready to learn something amazing today? 🚀")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="stat-card">
        <div class="stat-number">12</div>
        <div class="stat-label">📚 Topics Studied</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="stat-card">
        <div class="stat-number">86%</div>
        <div class="stat-label">🎯 Quiz Score</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="stat-card">
        <div class="stat-number">4.5h</div>
        <div class="stat-label">⏱️ Study Time</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="stat-card">
        <div class="stat-number">🔥 7</div>
        <div class="stat-label">Day Streak</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">⚡ Quick Actions</div>',
        unsafe_allow_html=True
    )

    a1, a2, a3 = st.columns(3)

    with a1:
        st.markdown("""
        <div class="tool-card">
        <div class="tool-icon">🤖</div>
        <h3>AI Tutor</h3>
        <p>Ask questions and learn concepts with your AI tutor.</p>
        </div>
        """, unsafe_allow_html=True)

    with a2:
        st.markdown("""
        <div class="tool-card">
        <div class="tool-icon">🎯</div>
        <h3>Quiz Arena</h3>
        <p>Challenge yourself with AI-generated quizzes.</p>
        </div>
        """, unsafe_allow_html=True)

    with a3:
        st.markdown("""
        <div class="tool-card">
        <div class="tool-icon">🧠</div>
        <h3>Flashcards</h3>
        <p>Turn difficult topics into memorable flashcards.</p>
        </div>
        """, unsafe_allow_html=True)

    b1, b2, b3 = st.columns(3)

    with b1:
        st.markdown("""
        <div class="tool-card">
        <div class="tool-icon">📄</div>
        <h3>PDF Brain</h3>
        <p>Upload notes and ask questions directly from your PDF.</p>
        </div>
        """, unsafe_allow_html=True)

    with b2:
        st.markdown("""
        <div class="tool-card">
        <div class="tool-icon">📝</div>
        <h3>Smart Notes</h3>
        <p>Convert lengthy notes into simple revision material.</p>
        </div>
        """, unsafe_allow_html=True)

    with b3:
        st.markdown("""
        <div class="tool-card">
        <div class="tool-icon">📅</div>
        <h3>Study Planner</h3>
        <p>Create a personalized AI study schedule.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">🏆 Achievements</div>',
        unsafe_allow_html=True
    )

    x1, x2, x3 = st.columns(3)

    with x1:
        st.markdown("""
        <div class="achievement">
        🥇<br>
        <b>First Steps</b><br>
        <small>Started learning</small>
        </div>
        """, unsafe_allow_html=True)

    with x2:
        st.markdown("""
        <div class="achievement">
        🔥<br>
        <b>7-Day Streak</b><br>
        <small>Keep going!</small>
        </div>
        """, unsafe_allow_html=True)

    with x3:
        st.markdown("""
        <div class="achievement">
        🧠<br>
        <b>Quick Learner</b><br>
        <small>100+ XP earned</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">💡 Tip of the Day</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="tip">
    💡 <b>Don't just read.</b> Try explaining what you learned
    in your own words. Teaching yourself is one of the best
    ways to remember concepts! 🧠✨
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# AI TUTOR
# ============================================================

elif page == "💬 AI Tutor":

    st.markdown(
        '<div class="section-title">🤖 AI Study Tutor</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="ai-panel">
    <h2>💬 Ask me anything!</h2>
    <p>I can explain difficult concepts in beginner-friendly language.</p>
    </div>
    """, unsafe_allow_html=True)

    question = st.text_area(
        "💭 Your Question",
        placeholder="Example: Explain Python variables with an easy example...",
        height=170
    )

    if st.button("🚀 Ask My AI Tutor", use_container_width=True):

        if not question.strip():
            st.warning("⚠️ Please enter a question.")

        else:
            with st.spinner("🤖 Thinking..."):

                try:

                    answer = ask_gemini(f"""
You are an expert but friendly AI Study Tutor.

Student question:
{question}

Explain in very simple language.

Use:

## 📖 Simple Explanation

## 💡 Easy Example

## ⭐ Important Points

## 📝 Quick Revision

## 🎯 One Question For Practice

Use emojis where appropriate.
""")

                    st.session_state.xp += 10
                    st.session_state.questions += 1

                    st.markdown(
                        '<div class="answer"><h2>🤖 AI Tutor Answer</h2></div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(answer)

                    st.success("🎉 +10 XP earned!")

                except Exception as e:
                    st.error("❌ AI could not answer right now.")
                    st.code(str(e))

# ============================================================
# EXPLAIN TOPIC
# ============================================================

elif page == "📖 Explain Topic":

    st.markdown(
        '<div class="section-title">📖 Topic Explainer</div>',
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "📚 Enter your topic",
        placeholder="Example: Data Structures"
    )

    level = st.selectbox(
        "🎓 Select difficulty",
        ["Beginner", "Intermediate", "Exam Preparation"]
    )

    if st.button("📖 Explain This Topic", use_container_width=True):

        if not topic.strip():
            st.warning("⚠️ Enter a topic first.")

        else:

            with st.spinner("🧠 Preparing explanation..."):

                answer = ask_gemini(f"""
Explain {topic} for a {level} student.

Use:

## 📖 What is it?

## 💡 Easy Explanation

## 🌍 Real-Life Example

## ⭐ Important Points

## 📝 Exam Notes

## 🎯 Quick Revision
""")

                st.session_state.xp += 10

                st.markdown(
                    '<div class="answer"><h2>📖 Topic Explained</h2></div>',
                    unsafe_allow_html=True
                )

                st.markdown(answer)

# ============================================================
# SMART NOTES
# ============================================================

elif page == "📝 Smart Notes":

    st.markdown(
        '<div class="section-title">📝 Smart Notes Generator</div>',
        unsafe_allow_html=True
    )

    notes = st.text_area(
        "📄 Paste your notes",
        height=280,
        placeholder="Paste your long notes here..."
    )

    if st.button("✨ Make Smart Notes", use_container_width=True):

        if not notes.strip():
            st.warning("⚠️ Paste some notes first.")

        else:

            with st.spinner("📝 Creating smart revision notes..."):

                answer = ask_gemini(f"""
Convert these study notes into useful revision material.

NOTES:

{notes}

Create:

## 📌 Key Concepts

## ⭐ Important Points

## 📖 Definitions

## 🧠 Easy Memory Tricks

## ❓ Possible Exam Questions

## 📝 Last-Minute Revision

Use simple language.
""")

                st.session_state.xp += 15

                st.markdown(
                    '<div class="answer"><h2>📝 Smart Revision Notes</h2></div>',
                    unsafe_allow_html=True
                )

                st.markdown(answer)

# ============================================================
# QUIZ ARENA
# ============================================================

elif page == "🎯 Quiz Arena":

    st.markdown(
        '<div class="section-title">🎯 Quiz Arena</div>',
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "📚 Quiz Topic",
        placeholder="Example: Python Basics"
    )

    difficulty = st.select_slider(
        "🔥 Difficulty",
        options=["Easy", "Medium", "Hard"],
        value="Easy"
    )

    number = st.slider(
        "🔢 Number of questions",
        5,
        15,
        10
    )

    if st.button("🎯 Start Quiz", use_container_width=True):

        if not topic.strip():
            st.warning("⚠️ Enter a topic.")

        else:

            with st.spinner("🎯 Building your quiz..."):

                answer = ask_gemini(f"""
Create a {number}-question MCQ quiz.

Topic: {topic}
Difficulty: {difficulty}

For every question provide:

Question

A.
B.
C.
D.

At the end provide:

## ✅ Answer Key

Also give a short explanation for each answer.
""")

                st.session_state.xp += 20

                st.markdown(
                    '<div class="answer"><h2>🎯 Quiz Arena</h2></div>',
                    unsafe_allow_html=True
                )

                st.markdown(answer)

                st.success("🏆 +20 XP earned!")

# ============================================================
# FLASHCARDS
# ============================================================

elif page == "🧠 Flashcards":

    st.markdown(
        '<div class="section-title">🧠 AI Flashcards</div>',
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "📚 Flashcard topic",
        placeholder="Example: C++ OOP"
    )

    number = st.slider(
        "🃏 Number of flashcards",
        5,
        20,
        10
    )

    if st.button("🧠 Generate Flashcards", use_container_width=True):

        if not topic.strip():
            st.warning("⚠️ Enter a topic.")

        else:

            with st.spinner("🧠 Creating flashcards..."):

                answer = ask_gemini(f"""
Create {number} useful study flashcards about {topic}.

Format:

### 🃏 Flashcard 1

**Question:** ...

**Answer:** ...

Keep answers short and useful for revision.
""")

                st.session_state.xp += 15

                st.markdown(answer)

# ============================================================
# PDF BRAIN
# ============================================================

elif page == "📄 PDF Brain":

    st.markdown(
        '<div class="section-title">📄 PDF Brain</div>',
        unsafe_allow_html=True
    )

    st.info("📚 Upload your textbook, notes, or study material.")

    uploaded = st.file_uploader(
        "📎 Upload PDF",
        type=["pdf"]
    )

    if uploaded:

        reader = PdfReader(uploaded)

        text = ""

        for page_pdf in reader.pages:

            extracted = page_pdf.extract_text()

            if extracted:
                text += extracted + "\n"

        st.success(
            f"✅ PDF loaded — {len(reader.pages)} pages found."
        )

        pdf_question = st.text_area(
            "💭 Ask something about your PDF",
            placeholder="Example: What are the main points of chapter 1?"
        )

        if st.button("📄 Ask PDF Brain", use_container_width=True):

            if not pdf_question.strip():
                st.warning("⚠️ Ask a question first.")

            else:

                with st.spinner("📖 Reading your PDF..."):

                    answer = ask_gemini(f"""
You are a PDF Study Assistant.

Use the following PDF content to answer the question.

PDF CONTENT:
{text[:40000]}

QUESTION:
{pdf_question}

Answ