import streamlit as st
from google import genai
from pypdf import PdfReader
import time
import random

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

* {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(59,130,246,0.18), transparent 30%),
        radial-gradient(circle at 90% 10%, rgba(139,92,246,0.18), transparent 30%),
        linear-gradient(135deg, #07152f 0%, #0b1f42 45%, #111b3d 100%);
    color: white;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #06132d, #0c2045);
    border-right: 1px solid rgba(255,255,255,0.12);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.hero {
    padding: 45px 30px;
    border-radius: 28px;
    text-align: center;
    margin-bottom: 28px;
    background:
        linear-gradient(135deg,
        rgba(30,64,175,0.90),
        rgba(76,29,149,0.88));
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 20px 60px rgba(0,0,0,0.35);
    animation: fadeIn 1s ease;
}

.hero-icon {
    font-size: 65px;
    animation: float 3s ease-in-out infinite;
}

.hero h1 {
    font-size: 46px;
    font-weight: 800;
    margin: 8px 0;
}

.hero p {
    font-size: 18px;
    color: #dbeafe;
}

@keyframes float {
    0%,100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

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

.section-title {
    font-size: 28px;
    font-weight: 700;
    margin: 28px 0 18px;
    color: #ffffff;
}

.feature-card {
    min-height: 170px;
    padding: 25px;
    border-radius: 22px;
    background: linear-gradient(
        145deg,
        rgba(30,64,175,0.55),
        rgba(15,23,42,0.85)
    );
    border: 1px solid rgba(147,197,253,0.20);
    box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    transition: all 0.3s ease;
    margin-bottom: 20px;
}

.feature-card:hover {
    transform: translateY(-7px);
    border-color: rgba(96,165,250,0.65);
    box-shadow: 0 20px 45px rgba(37,99,235,0.25);
}

.feature-icon {
    font-size: 42px;
}

.feature-title {
    font-size: 20px;
    font-weight: 700;
    margin-top: 10px;
}

.feature-text {
    color: #cbd5e1;
    font-size: 14px;
}

.ask-box {
    padding: 30px;
    border-radius: 25px;
    background: linear-gradient(
        145deg,
        rgba(15,23,42,0.92),
        rgba(30,41,59,0.90)
    );
    border: 1px solid rgba(96,165,250,0.25);
    box-shadow: 0 18px 45px rgba(0,0,0,0.30);
}

.answer-box {
    padding: 20px;
    border-radius: 20px;
    background: rgba(30,64,175,0.18);
    border-left: 5px solid #60a5fa;
    margin-top: 25px;
}

.stat-card {
    text-align: center;
    padding: 22px;
    border-radius: 20px;
    background: rgba(15,23,42,0.75);
    border: 1px solid rgba(255,255,255,0.10);
}

.stat-number {
    font-size: 30px;
    font-weight: 800;
    color: #93c5fd;
}

.stat-label {
    color: #cbd5e1;
    font-size: 13px;
}

.footer {
    text-align: center;
    margin-top: 50px;
    padding: 25px;
    color: #94a3b8;
}

div.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: 1px solid rgba(147,197,253,0.25);
    background: linear-gradient(135deg,#1d4ed8,#4f46e5);
    color: white;
    font-weight: 600;
    transition: all 0.25s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(59,130,246,0.35);
    border-color: #93c5fd;
}

textarea, input {
    border-radius: 12px !important;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# GEMINI CONNECTION
# ============================================================

if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔐 Gemini API key is missing.")
    st.info(
        "Go to Streamlit → Manage app → Settings → Secrets "
        "and add GEMINI_API_KEY."
    )
    st.stop()

try:
    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )
except Exception as e:
    st.error("❌ Could not connect to Gemini.")
    st.code(str(e))
    st.stop()

MODEL = "gemini-3.6-flash"

# ============================================================
# SESSION STATE
# ============================================================

if "question_count" not in st.session_state:
    st.session_state.question_count = 0

if "selected_tool" not in st.session_state:
    st.session_state.selected_tool = "💬 Ask AI"

if "messages" not in st.session_state:
    st.session_state.messages = []

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center;">
            <div style="font-size:55px;">🎓</div>
            <h2>Study Center</h2>
            <p style="color:#93c5fd;">Your learning dashboard</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🧠 Study Tools")

    tools = [
        "💬 Ask AI",
        "📄 PDF Study",
        "📝 Summarize Notes",
        "🎯 Generate Quiz",
        "🧠 Flashcards",
        "📅 Study Planner",
        "⏱️ Pomodoro Timer",
        "📊 Dashboard"
    ]

    for tool in tools:
        if st.button(tool, key="tool_" + tool):
            st.session_state.selected_tool = tool

    st.markdown("---")

    st.markdown("### 🌟 Features")

    st.markdown("""
    📚 Simple explanations

    🤖 Gemini AI powered

    📄 PDF learning

    🎯 Quiz practice

    🧠 Flashcards

    📅 Smart planning

    ⏱️ Focus timer
    """)

    st.markdown("---")

    st.caption("Made with ❤️ using Python + Streamlit + Gemini")

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-icon">📚</div>
        <h1>AI Study Assistant</h1>
        <p>Your Personal AI Tutor 🤖</p>
        <p>Learn • Practice • Revise • Succeed ✨</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# QUICK STATS
# ============================================================

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">🤖</div>
            <div class="stat-label">AI Tutor</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with s2:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">📄</div>
            <div class="stat-label">PDF Study</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with s3:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">🎯</div>
            <div class="stat-label">Quiz Practice</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with s4:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">🧠</div>
            <div class="stat-label">Smart Learning</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# FEATURE CARDS
# ============================================================

st.markdown(
    '<div class="section-title">✨ Explore Your Study Tools</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

cards = [
    ("💬", "Ask AI", "Ask any study question."),
    ("📄", "PDF Study", "Learn directly from PDFs."),
    ("📝", "Smart Notes", "Turn long notes into revision notes."),
    ("🎯", "Quiz", "Test your knowledge.")
]

for col, card in zip([c1, c2, c3, c4], cards):
    with col:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-icon">{card[0]}</div>
                <div class="feature-title">{card[1]}</div>
                <div class="feature-text">{card[2]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================================
# STUDY IMAGE
# ============================================================

st.image(
    "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1600&q=85",
    use_container_width=True
)

# ============================================================
# AI FUNCTION
# ============================================================

def ask_ai(prompt, instruction=""):
    full_prompt = f"""
You are a friendly AI Study Assistant.

Explain things to students using simple, clear language.

{instruction}

Student request:
{prompt}

Use:
📖 Simple Explanation
💡 Example
⭐ Important Points
📝 Quick Revision

Avoid unnecessarily complicated language.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=full_prompt
    )

    return response.text

# ============================================================
# ASK AI
# ============================================================

if st.session_state.selected_tool == "💬 Ask AI":

    st.markdown(
        '<div class="section-title">🤖 Ask Your AI Tutor</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="ask-box">', unsafe_allow_html=True)

    question = st.text_area(
        "💭 What would you like to learn?",
        placeholder="Example: Explain Python variables in very simple language...",
        height=150,
        key="main_question"
    )

    ask = st.button(
        "🤖 Ask AI",
        key="main_ask",
        use_container_width=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

    if ask:

        if not question.strip():
            st.warning("⚠️ Please enter your question first.")

        else:

            with st.spinner("🤖 Your AI tutor is thinking..."):

                try:
                    answer = ask_ai(question)
                    st.session_state.question_count += 1

                    st.markdown(
                        """
                        <div class="answer-box">
                            <h2>📖 AI Tutor Answer</h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(answer)
                    st.success("✅ Answer ready! Keep learning 🚀")

                except Exception as e:
                    st.error("❌ Gemini could not answer right now.")
                    st.code(str(e))

# ============================================================
# PDF STUDY
# ============================================================

elif st.session_state.selected_tool == "📄 PDF Study":

    st.markdown(
        '<div class="section-title">📄 Study From Your PDF</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "📚 Upload your study PDF",
        type=["pdf"]
    )

    if uploaded_file:

        try:

            reader = PdfReader(uploaded_file)

            pdf_text = ""

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    pdf_text += page_text + "\n"

            st.success(
                f"✅ PDF loaded successfully — {len(reader.pages)} page(s)"
            )

            pdf_question = st.text_area(
                "💭 Ask something about your PDF",
                placeholder="Example: Explain the main topic of this PDF."
            )

            if st.button("🤖 Ask PDF", use_container_width=True):

                if not pdf_question.strip():
                    st.warning("⚠️ Please enter a question.")

                else:

                    with st.spinner("📚 Reading your PDF..."):

                        try:

                            prompt = f"""
You are a PDF study assistant.

Use the following PDF content to answer the question.

PDF CONTENT:
{pdf_text[:50000]}

QUESTION:
{pdf_question}

Answer in simple student-friendly language.
"""

                            response = client.models.generate_content(
                                model=MODEL,
                                contents=prompt
                            )

                            st.markdown(
                                '<div class="answer-box"><h2>📖 PDF Answer</h2></div>',
                                unsafe_allow_html=True
                            )

                            st.markdown(response.text)

                        except Exception as e:
                            st.error("❌ Could not process the PDF.")
                            st.code(str(e))

        except Exception as e:
            st.error("❌ Could not read this PDF.")
            st.code(str(e))

# ============================================================
# SUMMARIZE NOTES
# ============================================================

elif st.session_state.selected_tool == "📝 Summarize Notes":

    st.markdown(
        '<div class="section-title">📝 Smart Notes Summarizer</div>',
        unsafe_allow_html=True
    )

    notes = st.text_area(
        "📚 Paste your study notes",
        placeholder="Paste your chapter or class notes here...",
        height=250
    )

    if st.button("✨ Summarize Notes", use_container_width=True):

        if not notes.strip():
            st.warning("⚠️ Please paste some notes first.")

        else:

            with st.spinner("📝 Creating your revision notes..."):

                try:

                    prompt = f"""
Summarize the following student notes.

NOTES:
{notes}

Create:

📌 Key Concepts
⭐ Important Points
📝 Short Revision Notes
❓ Possible Exam Questions

Use very simple language.
"""

                    response = client.models.generate_content(
                        model=MODEL,
                        contents=prompt
                    )

                    st.markdown(
                        '<div class="answer-box"><h2>📝 Smart Summary</h2></div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(response.text)

                except Exception as e:
                    st.error("❌ Could not summarize notes.")
                    st.code(str(e))

# ============================================================
# QUIZ
# ============================================================

elif st.session_state.selected_tool == "🎯 Generate Quiz":

    st.markdown(
        '<div class="section-title">🎯 AI Quiz Generator</div>',
        unsafe_allow_html=True
    )

    quiz_topic = st.text_input(
        "📚 Quiz Topic",
        placeholder="Example: Python Basics"
    )

    difficulty = st.selectbox(
        "🎚️ Difficulty",
        ["Beginner", "Intermediate", "Advanced"]
    )

    number = st.slider(
        "🔢 Number of questions",
        3,
        15,
        5
    )

    if st.button("🚀 Generate Quiz", use_container_width=True):

        if not quiz_topic.strip():
            st.warning("⚠️ Please enter a quiz topic.")

        else:

            with st.spinner("🎯 Creating your quiz..."):

                try:

                    prompt = f"""
Create a multiple-choice quiz.

Topic: {quiz_topic}
Difficulty: {difficulty}
Number of questions: {number}

For each question give:

Question
A.
B.
C.
D.

After all questions provide:
✅ Correct Answers
💡 Short Explanations

Make it suitable for students.
"""

                    response = client.models.generate_content(
                        model=MODEL,
                        contents=prompt
                    )

                    st.markdown(
                        '<div class="answer-box"><h2>🎯 Your Quiz</h2></div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(response.text)

                except Exception as e:
                    st.error("❌ Could not generate quiz.")
                    st.code(str(e))

# ============================================================
# FLASHCARDS
# ============================================================

elif st.session_state.selected_tool == "🧠 Flashcards":

    st.markdown(
        '<div class="section-title">🧠 AI Flashcards</div>',
        unsafe_allow_html=True
    )

    flash_topic = st.text_input(
        "📚 Topic",
        placeholder="Example: Data Structures"
    )

    if st.button("🧠 Create Flashcards", use_container_width=True):

        if not flash_topic.strip():
            st.warning("⚠️ Enter a topic first.")

        else:

            with st.spinner("🧠 Creating flashcards..."):

                try:

                    prompt = f"""
Create 10 study flashcards about:

{flash_topic}

Format:

### 🃏 Card 1
❓ Question:
💡 Answer:

Keep each answer short and easy to remember.
"""

                    response = client.models.generate_content(
                        model=MODEL,
                        contents=prompt
                    )

                    st.markdown(response.text)

                except Exception as e:
                    st.error("❌ Could not create flashcards.")
                    st.code(str(e))

# ============================================================
# STUDY PLANNER
# ============================================================

elif st.session_state.selected_tool == "📅 Study Planner":

    st.markdown(
        '<div class="section-title">📅 Smart Study Planner</div>',
        unsafe_allow_html=True
    )

    subject = st.text_input(
        "📚 Subject",
        placeholder="Example: Python"
    )

    days = st.number_input(
        "📆 Number of days",
        1,
        30,
        7
    )

    hours = st.number_input(
        "⏰ Study hours per day",
        1,
        12,
        2
    )

    if st.button("🚀 Create Study Plan", use_container_width=True):

        if not subject.strip():
            st.warning("⚠️ Enter a subject first.")

        else:

            with st.spinner("📅 Creating your personalized plan..."):

                try:

                    prompt = f"""
Create a realistic study plan.

Subject: {subject}
Days: {days}
Hours per day: {hours}

Give a day-by-day schedule.

Include:
📚 Topics
⏰ Study time
📝 Practice
🔄 Revision
🎯 Daily goal

Use simple language.
"""

                    response = client.models.generate_content(
                        model=MODEL,
                        contents=prompt
                    )

                    st.markdown(response.text)

                except Exception as e:
                    st.error("❌ Could not create study plan.")
                    st.code(str(e))

# ============================================================
# POMODORO TIMER
# ============================================================

elif st.session_state.selected_tool == "⏱️ Pomodoro Timer":

    st.markdown(
        '<div class="section-title">⏱️ Focus Timer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="feature-card" style="text-align:center;">
            <div style="font-size:65px;">🍅</div>
            <h2>Pomodoro Study Session</h2>
            <p>Focus for 25 minutes, then take a short break.</p>
        </div>
 
    
    
        
