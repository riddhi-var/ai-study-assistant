

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
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 20%, rgba(79,70,229,0.22), transparent 25%),
        radial-gradient(circle at 90% 15%, rgba(6,182,212,0.16), transparent 25%),
        radial-gradient(circle at 50% 90%, rgba(124,58,237,0.18), transparent 30%),
        linear-gradient(135deg, #020617 0%, #0f172a 45%, #111827 100%);
    background-attachment: fixed;
}

@keyframes float {
    0%, 100% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(-10px);
    }
}

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

.hero {
    position: relative;
    overflow: hidden;
    padding: 50px 25px;
    margin: 15px 0 30px 0;
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
    animation: fadeUp 0.8s ease, gradientMove 10s ease infinite;
    box-shadow: 0 25px 80px rgba(0,0,0,0.35);
}

.hero-icon {
    font-size: 70px;
    display: inline-block;
    animation: float 3s ease-in-out infinite;
}

.hero h1 {
    font-size: 48px;
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
    color: #cbd5e1;
    font-size: 18px;
}

.section-title {
    font-size: 28px;
    font-weight: 800;
    margin: 30px 0 18px 0;
    color: #f8fafc;
}

.tool-card {
    min-height: 175px;
    padding: 22px;
    border-radius: 22px;
    background:
        linear-gradient(
            135deg,
            rgba(30,41,59,0.80),
            rgba(15,23,42,0.65)
        );
    backdrop-filter: blur(15px);
    border: 1px solid rgba(129,140,248,0.22);
    box-shadow: 0 15px 40px rgba(0,0,0,0.25);
    transition: 0.3s ease;
    animation: fadeUp 0.7s ease;
}

.tool-card:hover {
    transform: translateY(-8px);
    border-color: rgba(129,140,248,0.75);
    box-shadow: 0 20px 50px rgba(79,70,229,0.28);
}

.tool-icon {
    font-size: 42px;
    display: inline-block;
    animation: float 3s ease-in-out infinite;
}

.tool-title {
    font-size: 20px;
    font-weight: 800;
    margin-top: 10px;
    color: white;
}

.tool-text {
    color: #94a3b8;
    margin-top: 7px;
    line-height: 1.5;
}

.answer-box {
    padding: 20px;
    margin: 20px 0;
    border-radius: 20px;
    background:
        linear-gradient(
            135deg,
            rgba(30,41,59,0.90),
            rgba(49,46,129,0.65)
        );
    border: 1px solid rgba(129,140,248,0.40);
}

.sidebar-title {
    font-size: 24px;
    font-weight: 900;
    color: white;
    padding: 10px 0 20px 0;
}

.sidebar-card {
    padding: 14px;
    margin: 8px 0;
    border-radius: 15px;
    background: rgba(30,41,59,0.65);
    border: 1px solid rgba(129,140,248,0.20);
}

.stButton > button {
    width: 100%;
    min-height: 46px;
    border-radius: 14px;
    border: 1px solid rgba(129,140,248,0.40);
    background:
        linear-gradient(
            90deg,
            #312e81,
            #4f46e5,
            #7c3aed
        );
    color: white;
    font-weight: 700;
    transition: 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(99,102,241,0.45);
}

.stTextArea textarea,
.stTextInput input {
    background: rgba(15,23,42,0.85) !important;
    color: #f8fafc !important;
    border-radius: 14px !important;
    border: 1px solid rgba(129,140,248,0.35) !important;
}

.footer {
    margin-top: 50px;
    padding: 30px;
    text-align: center;
    border-radius: 22px;
    background: rgba(15,23,42,0.80);
    border: 1px solid rgba(129,140,248,0.20);
}

@media (max-width: 768px) {
    .hero {
        padding: 35px 15px;
    }

    .hero h1 {
        font-size: 34px;
    }

    .hero-icon {
        font-size: 52px;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# GEMINI CONNECTION
# ============================================================

api_key = None

try:
    api_key = st.secrets.get("GEMINI_API_KEY")
except Exception:
    api_key = None


if not api_key:
    st.sidebar.warning("🔐 Gemini API key not found.")

    api_key = st.sidebar.text_input(
        "Enter Gemini API Key",
        type="password",
        help="For deployment, add GEMINI_API_KEY to Streamlit Secrets.",
    )


if not api_key:
    st.error("🔐 Gemini API key is required to use AI features.")
    st.info(
        "For Streamlit Cloud, add GEMINI_API_KEY in "
        "Settings → Secrets."
    )
    st.stop()


try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("❌ Could not connect to Gemini.")
    st.code(str(e))
    st.stop()


MODEL = "gemini-2.5-flash"


# ============================================================
# HELPER FUNCTION
# ============================================================

def ask_gemini(prompt):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    if response.text:
        return response.text

    return "Sorry, I could not generate an answer."


# ============================================================
# SESSION STATE
# ============================================================

if "tool" not in st.session_state:
    st.session_state.tool = "ask"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🎓 Study Center</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-card">
        💬 <b>Ask AI</b><br>
        <small>Ask any study question.</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-card">
        📄 <b>PDF Study</b><br>
        <small>Ask questions from your PDF.</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-card">
        🎯 <b>Quiz</b><br>
        <small>Practice your knowledge.</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-card">
        📝 <b>Smart Notes</b><br>
        <small>Summarize your notes.</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-card">
        🧠 <b>Flashcards</b><br>
        <small>Revise concepts faster.</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-card">
        📅 <b>Study Planner</b><br>
        <small>Create a study routine.</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown("### 🌟 Features")

    st.markdown(
        """
        📚 Simple explanations

        🤖 AI-powered learning

        📄 PDF study assistant

        🎯 Quiz practice

        🧠 Flashcards

        📅 Study planner

        ⏱️ Focus timer
        """
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

        <p>
            Learn • Practice • Revise • Succeed ✨
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# TOOL CARDS
# ============================================================

st.markdown(
    '<div class="section-title">🚀 Choose Your Study Tool</div>',
    unsafe_allow_html=True,
)

tool1, tool2, tool3, tool4 = st.columns(4)

with tool1:
    st.markdown(
        """
        <div class="tool-card">
            <div class="tool-icon">💬</div>
            <div class="tool-title">Ask AI</div>
            <div class="tool-text">
                Ask anything about your studies.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tool2:
    st.markdown(
        """
        <div class="tool-card">
            <div class="tool-icon">📄</div>
            <div class="tool-title">Study PDF</div>
            <div class="tool-text">
                Upload notes and ask questions.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tool3:
    st.markdown(
        """
        <div class="tool-card">
            <div class="tool-icon">🎯</div>
            <div class="tool-title">Quiz</div>
            <div class="tool-text">
                Create quizzes for practice.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tool4:
    st.markdown(
        """
        <div class="tool-card">
            <div class="tool-icon">🧠</div>
            <div class="tool-title">Flashcards</div>
            <div class="tool-text">
                Learn using quick revision cards.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# NAVIGATION
# ============================================================

st.markdown("### 🎮 Open a Tool")

b1, b2, b3, b4, b5, b6, b7 = st.columns(7)

with b1:
    if st.button("💬 Ask AI"):
        st.session_state.tool = "ask"

with b2:
    if st.button("📄 PDF"):
        st.session_state.tool = "pdf"

with b3:
    if st.button("🎯 Quiz"):
        st.session_state.tool = "quiz"

with b4:
    if st.button("📝 Notes"):
        st.session_state.tool = "notes"

with b5:
    if st.button("🧠 Cards"):
        st.session_state.tool = "flash"

with b6:
    if st.button("📅 Planner"):
        st.session_state.tool = "plan"

with b7:
    if st.button("⏱️ Timer"):
        st.session_state.tool = "timer"


# ============================================================
# ASK AI
# ============================================================

if st.session_state.tool == "ask":

    st.markdown(
        '<div class="section-title">🤖 Ask Your AI Tutor</div>',
        unsafe_allow_html=True,
    )

    question = st.text_area(
        "💭 Your Question",
        placeholder=(
            "Example: Explain Python variables "
            "in very simple language..."
        ),
        height=150,
    )

    if st.button("🚀 Ask AI Tutor", key="ask_main"):

        if not question.strip():
            st.warning("⚠️ Please enter your question first.")

        else:

            prompt = f"""
You are a friendly AI Study Assistant.

Student question:
{question}

Explain the answer in very simple beginner-friendly language.

Use this structure:

## 📖 Simple Explanation

## 💡 Example

## 📝 Important Points

## 🎯 Quick Revision

## ❓ One Practice Question
"""

            with st.spinner("🤖 AI tutor is thinking..."):

                try:
                    answer = ask_gemini(prompt)

                    st.markdown(
                        """
                        <div class="answer-box">
                            <h2>📖 AI Tutor Answer</h2>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown(answer)

                    st.success(
                        "✅ Answer generated! Keep learning 🚀"
                    )

                except Exception as e:
                    st.error("❌ Gemini could not answer.")
                    st.code(str(e))


# ============================================================
# PDF STUDY
# ============================================================

elif st.session_state.tool == "pdf":

    st.markdown(
        '<div class="section-title">📄 Study From Your PDF</div>',
        unsafe_allow_html=True,
    )

    uploaded_pdf = st.file_uploader(
        "📚 Upload your study PDF",
        type=["pdf"],
    )

    if uploaded_pdf:

        try:
            reader = PdfReader(uploaded_pdf)

            pdf_text = ""

            for page in reader.pages:
                extracted = page.extract_text()

                if extracted:
                    pdf_text += extracted + "\n"

            if not pdf_text.strip():
                st.warning(
                    "⚠️ No readable text was found in this PDF."
                )
            else:

                st.success(
                    f"✅ PDF loaded successfully! "
                    f"{len(reader.pages)} page(s) found."
                )

                pdf_question = st.text_area(
                    "💭 Ask a question about your PDF",
                    placeholder=(
                        "Example: What are the main points?"
                    ),
                    height=120,
                )

                if st.button("📚 Ask From PDF"):

                    if not pdf_question.strip():
                        st.warning(
                            "⚠️ Please enter a question."
                        )

                    else:

                        prompt = f"""
You are a study assistant.

Use the PDF content below to answer the student's question.

PDF content:
{pdf_text[:40000]}

Student question:
{pdf_question}

Answer in simple language.

If the answer cannot be found in the PDF,
clearly say that it is not available in the provided PDF.
"""

                        with st.spinner(
                            "📖 Reading your PDF..."
                        ):

                            try:
                                answer = ask_gemini(prompt)

                                st.markdown(
                                    """
                                    <div class="answer-box">
                                        <h2>📚 PDF Answer</h2>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                                st.markdown(answer)

                            except Exception as e:
                                st.error(
                                    "❌ Could not process the PDF."
                                )
                                st.code(str(e))

        except Exception as e:
            st.error("❌ Could not read this PDF.")
            st.code(str(e))


# ============================================================
# QUIZ
# ============================================================

elif st.session_state.tool == "quiz":

    st.markdown(
        '<div class="section-title">🎯 AI Quiz Generator</div>',
        unsafe_allow_html=True,
    )

    quiz_topic = st.text_input(
        "📚 Quiz Topic",
        placeholder="Example: Python Basics",
    )

    quiz_level = st.selectbox(
        "📊 Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced",
        ],
    )

    number_of_questions = st.slider(
        "🔢 Number of Questions",
        5,
        20,
        10,
    )

    if st.button("🎯 Generate Quiz"):

        if not quiz_topic.strip():
            st.warning("⚠️ Enter a topic first.")

        else:

            prompt = f"""
Create a {number_of_questions}-question
multiple-choice quiz.

Topic:
{quiz_topic}

Difficulty:
{quiz_level}

For every question provide:

1. Question
2. Option A
3. Option B
4. Option C
5. Option D

After all questions provide:

## Answer Key

Keep the quiz educational and clear.
"""

            with st.spinner("🎯 Creating your quiz..."):

                try:
                    answer = ask_gemini(prompt)

                    st.markdown(
                        """
                        <div class="answer-box">
                            <h2>🎯 Your Quiz</h2>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown(answer)

                except Exception as e:
                    st.error("❌ Quiz generation failed.")
                    st.code(str(e))


# ============================================================
# SMART NOTES
# ============================================================

elif st.session_state.tool == "notes":

    st.markdown(
        '<div class="section-title">📝 Smart Notes Summarizer</div>',
        unsafe_allow_html=True,
    )

    notes = st.text_area(
        "📖 Paste your study notes",
        height=280,
        placeholder="Paste your long study notes here...",
    )

    if st.button("✨ Summarize Notes"):

        if not notes.strip():
            st.warning("⚠️ Please paste your notes.")

        else:

            prompt = f"""
Summarize the following study notes
in simple and exam-friendly language.

Notes:
{notes}

Use this structure:

## 📌 Key Concepts

## ⭐ Important Points

## 📝 Revision Notes

## ❓ Possible Exam Questions

## 🎯 Quick Revision
"""

            with st.spinner("📝 Creating your summary..."):

                try:
                    answer = ask_gemini(prompt)

                    st.markdown(
                        """
                        <div class="answer-box">
                            <h2>📝 Smart Summary</h2>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown(answer)

                except Exception as e:
                    st.error(
                        "❌ Could not summarize notes."
                    )
                    st.code(str(e))


# ============================================================
# FLASHCARDS
# ============================================================

elif st.session_state.tool == "flash":

    st.markdown(
        '<div class="section-title">🧠 AI Flashcard Generator</div>',
        unsafe_allow_html=True,
    )

    flash_topic = st.text_input(
        "📚 Flashcard Topic",
        placeholder="Example: C++ OOP",
    )

    number_of_cards = st.slider(
        "🔢 Number of Flashcards",
        5,
        20,
        10,
    )

    if st.button("🧠 Create Flashcards"):

        if not flash_topic.strip():
            st.warning("⚠️ Enter a topic first.")

        else:

            prompt = f"""
Create {number_of_cards} useful study
flashcards for:

Topic:
{flash_topic}

Format each flashcard like this:

### 🟦 Card 1

**Question:** ...

**Answer:** ...

Use simple language and focus on
important concepts.
"""

                            flash_topic = st.text_input(
        "📚 Flashcard Topic",
        placeholder="Example: C++ OOP",
    )

    number_of_cards = st.slider(
        "🔢 Number of Flashcards",
        5,
        20,
        10,
    )

    if st.button("🧠 Create Flashcards"):

        if not flash_topic.strip():
            st.warning("⚠️ Enter a topic first.")

        else:

            prompt = f"""
Create {number_of_cards} useful study
flashcards for:

Topic:
{flash_topic}

Format each flashcard like this:

### 🟦 Card 1

**Question:** ...

**Answer:** ...

Use simple language and focus on
important concepts.
"""

            with st.spinner("🧠 Creating flashcards..."):

                try:
                    answer = ask_gemini(prompt)

                    st.markdown(
                        """
                        <div class="answer-box">
                            <h2>🧠 Flashcards</h2>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown(answer)

                except Exception as e:
                    st.error("❌ Could not create flashcards.")
                    st.code(str(e))


# ============================================================
# STUDY PLANNER
# =============================================================
elif st.session_state.tool == "plan":

    st.markdown(
        '<div class="section-title">📅 Smart Study Planner</div>',
        unsafe_allow_html=True,
    )

    subject = st.text_input(
        "📚 Subject",
        placeholder="Example: Python",
    )

    days = st.number_input(
        "📆 Number of Days",
        min_value=1,
        max_value=30,
        value=7,
    )

    hours = st.number_input(
        "⏰ Study Hours Per Day",
        min_value=1,
        max_value=12,
        value=2,
    )

    level = st.selectbox(
        "📊 Your Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced",
        ],
    )

    if st.button("🚀 Create Study Plan"):

        if not subject.strip():
            st.warning("⚠️ Enter a subject first.")

        else:

            prompt = f"""
Create a realistic study plan.

Subject:
{subject}

Number of days:
{days}

Study hours per day:
{hours}

Student level:
{level}

Create a day-by-day plan.

Include:
- Topics
- Study time
- Practice
- Revision
- Small daily goals

Keep it beginner-friendly and practical.
"""

            with st.spinner("📅 Creating your study plan..."):

                try:
                    answer = ask_gemini(prompt)

                    st.markdown(
                        """
                        <div class="answer-box">
                            <h2>📅 Your Study Plan</h2>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown(answer)

                except Exception as e:
                    st.error("❌ Could not create study plan.")
                    st.code(str(e))


# ============================================================
# POMODORO TIMER
# ============================================================

elif st.session_state.tool == "timer":

    st.markdown(
        '<div class="section-title">⏱️ Focus Timer</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Use the Pomodoro technique to study with focused sessions."
    )

    timer_minutes = st.slider(
        "⏰ Timer Duration",
        min_value=1,
        max_value=60,
        value=25,
    )

    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False

    if "timer_end" not in st.session_state:
        st.session_state.timer_end = None

    col1, col2 = st.columns(2)

    with col1:
        start_timer = st.button(
            "▶️ Start Timer",
            key="start_timer",
        )

    with col2:
        stop_timer = st.button(
            "⏹️ Stop Timer",
            key="stop_timer",
        )

    if start_timer:
        st.session_state.timer_running = True
        st.session_state.timer_end = (
            time.time() + timer_minutes * 60
        )

    if stop_timer:
        st.session_state.timer_running = False
        st.session_state.timer_end = None
        st.info("⏹️ Timer stopped.")

    if (
        st.session_state.timer_running
        and st.session_state.timer_end
    ):

        remaining = int(
            st.session_state.timer_end - time.time()
        )

        if remaining <= 0:

            st.session_state.timer_running = False
            st.session_state.timer_end = None

            st.success("🎉 Time's up! Great work!")
            st.balloons()

        else:

            minutes_left = remaining // 60
            seconds_left = remaining % 60

            st.markdown(
                f"""
                <div class="answer-box"
                     style="text-align:center;">
                    <h1>
                        ⏱️ {minutes_left:02d}:{seconds_left:02d}
                    </h1>
                    <p>Stay focused 🚀</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            time.sleep(1)
            st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        <h2>📚 AI Study Assistant</h2>

        <p>
            Learn smarter • Practice better • Achieve more 🚀
        </p>

        <p>
            Made with ❤️ using Python, Streamlit and Gemini AI
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
