import streamlit as st
from google import genai
from pypdf import PdfReader

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS - NAVY BLUE + PURPLE + ANIMATIONS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

/* Main background */
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(79, 70, 229, 0.16), transparent 28%),
        radial-gradient(circle at 90% 15%, rgba(37, 99, 235, 0.14), transparent 28%),
        linear-gradient(135deg, #f8faff 0%, #eef2ff 50%, #f8faff 100%);
}

/* Hide Streamlit decoration */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* Main container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

/* Animated hero */
.hero {
    background: linear-gradient(135deg, #0f172a, #172554, #312e81, #1e3a8a);
    background-size: 300% 300%;
    animation: gradientMove 8s ease infinite;
    padding: 45px 35px;
    border-radius: 28px;
    text-align: center;
    color: white;
    box-shadow: 0 18px 45px rgba(15, 23, 42, 0.25);
    margin-bottom: 30px;
    overflow: hidden;
    position: relative;
}

.hero:before {
    content: "";
    position: absolute;
    width: 180px;
    height: 180px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
    top: -70px;
    left: -60px;
    animation: floating 5s ease-in-out infinite;
}

.hero:after {
    content: "";
    position: absolute;
    width: 220px;
    height: 220px;
    background: rgba(129,140,248,0.12);
    border-radius: 50%;
    bottom: -100px;
    right: -70px;
    animation: floating 6s ease-in-out infinite reverse;
}

.hero-icon {
    font-size: 60px;
    animation: bounce 2.5s ease-in-out infinite;
}

.hero h1 {
    font-size: 44px;
    margin: 8px 0;
    font-weight: 800;
    letter-spacing: -1px;
}

.hero p {
    font-size: 18px;
    color: #dbeafe;
    margin: 5px;
}

.hero-small {
    font-size: 14px !important;
    color: #c7d2fe !important;
}

/* Section headings */
.section-title {
    color: #172554;
    font-size: 28px;
    font-weight: 800;
    margin: 30px 0 18px 0;
}

/* Feature cards */
.feature-card {
    background: rgba(255,255,255,0.92);
    border: 1px solid #dbeafe;
    border-radius: 20px;
    padding: 25px 20px;
    min-height: 155px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(30,41,59,0.08);
    transition: all 0.35s ease;
    animation: cardAppear 0.8s ease both;
}

.feature-card:hover {
    transform: translateY(-9px) scale(1.02);
    box-shadow: 0 18px 35px rgba(30,64,175,0.18);
    border-color: #818cf8;
}

.feature-icon {
    font-size: 40px;
    margin-bottom: 8px;
}

.feature-title {
    color: #1e3a8a;
    font-size: 19px;
    font-weight: 700;
}

.feature-text {
    color: #64748b;
    font-size: 13px;
    line-height: 1.6;
}

/* AI tutor box */
.tutor-box {
    background: linear-gradient(135deg, #ffffff, #eef2ff);
    border: 2px solid #c7d2fe;
    border-radius: 25px;
    padding: 28px;
    box-shadow: 0 12px 35px rgba(49,46,129,0.12);
    margin-top: 15px;
    transition: 0.35s ease;
}

.tutor-box:hover {
    box-shadow: 0 18px 45px rgba(49,46,129,0.18);
}

/* Answer box */
.answer-box {
    background: linear-gradient(135deg, #eef2ff, #eff6ff);
    border-left: 6px solid #312e81;
    border-radius: 18px;
    padding: 20px;
    margin-top: 25px;
    box-shadow: 0 10px 30px rgba(30,64,175,0.12);
    animation: slideUp 0.6s ease;
}

/* Image */
.study-image {
    border-radius: 25px;
    box-shadow: 0 15px 40px rgba(15,23,42,0.18);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #1e3a8a, #312e81) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 12px 20px !important;
    font-weight: 700 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 7px 18px rgba(30,58,138,0.20) !important;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    background: linear-gradient(135deg, #312e81, #4338ca) !important;
    box-shadow: 0 12px 25px rgba(49,46,129,0.30) !important;
}

.stButton > button:active {
    transform: scale(0.97) !important;
}

/* Text areas and inputs */
.stTextArea textarea,
.stTextInput input,
.stNumberInput input {
    border: 2px solid #c7d2fe !important;
    border-radius: 14px !important;
    background: white !important;
    transition: 0.3s ease !important;
}

.stTextArea textarea:focus,
.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: #4f46e5 !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,0.12) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #172554, #1e1b4b) !important;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.sidebar-title {
    font-size: 25px;
    font-weight: 800;
    padding: 10px 0 20px 0;
    text-align: center;
}

/* Sidebar info cards */
section[data-testid="stSidebar"] .stAlert {
    background: rgba(255,255,255,0.10) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 14px !important;
}

/* Tips */
.tip-card {
    background: white;
    border-radius: 18px;
    padding: 22px;
    min-height: 140px;
    border: 1px solid #e0e7ff;
    box-shadow: 0 8px 25px rgba(30,41,59,0.07);
    transition: 0.3s ease;
}

.tip-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 15px 30px rgba(30,64,175,0.14);
}

/* Footer */
.footer {
    margin-top: 50px;
    padding: 30px;
    border-radius: 22px;
    text-align: center;
    background: linear-gradient(135deg, #0f172a, #1e1b4b);
    color: #c7d2fe;
}

.footer-title {
    color: white;
    font-size: 22px;
    font-weight: 800;
}

/* Animations */
@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes floating {
    0%,100% { transform: translateY(0px); }
    50% { transform: translateY(18px); }
}

@keyframes bounce {
    0%,100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

@keyframes cardAppear {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(25px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">
    <div class="hero-icon">📚</div>
    <h1>AI Study Assistant</h1>
    <p>Your Personal AI Tutor 🤖</p>
    <p class="hero-small">Learn • Practice • Revise • Succeed ✨</p>
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

    st.info("💬 Ask AI\n\nAsk any study question.")

    st.success("📖 Explain Topic\n\nUnderstand difficult topics.")

    st.warning("📝 Summarize\n\nGet short revision notes.")

    st.error("🎯 Generate Quiz\n\nPractice your knowledge.")

    st.markdown("---")

    st.markdown("### 🌟 Features")

    st.markdown("""
    📚 Easy explanations

    🤖 AI-powered answers

    💡 Simple language

    📝 Study-friendly notes

    🎯 Exam preparation

    ⚡ Quick revision
    """)

    st.markdown("---")

    st.caption("Made with ❤️ using Python + Streamlit + Gemini")

# ============================================================
# FEATURE SECTION
# ============================================================

st.markdown(
    '<div class="section-title">✨ What can I help you with?</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💬</div>
        <div class="feature-title">Ask AI</div>
        <div class="feature-text">
        Ask questions about your subjects.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📖</div>
        <div class="feature-title">Explain</div>
        <div class="feature-text">
        Understand difficult concepts easily.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📝</div>
        <div class="feature-title">Summarize</div>
        <div class="feature-text">
        Turn long topics into simple notes.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">Practice</div>
        <div class="feature-text">
        Generate questions for revision.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# STUDY IMAGE
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

st.image(
    "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1600&q=85",
    use_container_width=True
)

# ============================================================
# AI TUTOR
# ============================================================

st.markdown(
    '<div class="section-title">🤖 Ask Your AI Tutor</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="tutor-box">

<h3 style="color:#1e3a8a;">💡 Have a doubt? Ask me!</h3>

<p style="color:#64748b;">
I can explain programming, mathematics, science,
engineering and many other study topics in simple language.
</p>

</div>
""", unsafe_allow_html=True)

question = st.text_area(
    "💭 Your Question",
    placeholder="Example: Explain Python variables in very simple language...",
    height=150
)

# ============================================================
# MAIN BUTTONS
# ============================================================

button1, button2, button3 = st.columns(3)

with button1:
    ask_ai = st.button(
        "🤖 Ask AI",
        use_container_width=True,
        key="ask_ai"
    )

with button2:
    explain_topic = st.button(
        "📖 Explain Topic",
        use_container_width=True,
        key="explain_topic"
    )

with button3:
    generate_quiz = st.button(
        "🎯 Generate Quiz",
        use_container_width=True,
        key="generate_quiz"
    )

# ============================================================
# GEMINI FUNCTION
# ============================================================

def ask_gemini(prompt):

    api_key = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(
        api_key=api_key
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text


# ============================================================
# ASK AI
# ============================================================

if ask_ai:

    if not question.strip():

        st.warning("⚠️ Please enter your question first.")

    else:

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

            try:

                answer = ask_gemini(prompt)

                st.markdown("""
                <div class="answer-box">
                <h2 style="color:#312e81;">📖 AI Tutor Answer</h2>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(answer)

                st.success("✅ Done! Keep learning 🚀")

            except KeyError:

                st.error(
                    "🔐 Gemini API key is missing. "
                    "Please add GEMINI_API_KEY in Streamlit Secrets."
                )

            except Exception as e:

                st.error("❌ Something went wrong while connecting to Gemini.")

                st.code(str(e))


# ============================================================
# EXPLAIN TOPIC
# ============================================================

if explain_topic:

    if not question.strip():

        st.warning(
            "📖 Please enter a topic in the question box first."
        )

    else:

        prompt = f"""
You are a friendly AI teacher.

Explain this topic to a beginner:

{question}

Use this format:

## 📖 What is it?

## 💡 Easy Explanation

## 🧠 Real-Life Example

## 📝 Important Points

## 🎯 Quick Revision

Use simple language and helpful emojis.
"""

        with st.spinner("📖 Explaining the topic..."):

            try:

                answer = ask_gemini(prompt)

                st.markdown("""
                <div class="answer-box">
                <h2 style="color:#312e81;">📖 Topic Explanation</h2>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(answer)

            except Exception as e:

                st.error("❌ Could not explain the topic.")

                st.code(str(e))


# ============================================================
# QUIZ GENERATOR
# ============================================================

if generate_quiz:

    quiz_topic = st.text_input(
        "🎯 Enter topic for your quiz",
        placeholder="Example: Python Basics"
    )

    quiz_level = st.selectbox(
        "📊 Select difficulty",
        [
            "🟢 Beginner",
            "🟡 Intermediate",
            "🔴 Advanced"
        ]
    )

    if st.button(
        "🚀 Create My Quiz",
        use_container_width=True,
        key="create_quiz"
    ):

        if not quiz_topic.strip():

            st.warning("⚠️ Please enter a quiz topic.")

        else:

            prompt = f"""
Create a 10-question multiple-choice quiz.

Topic: {quiz_topic}

Difficulty:
{quiz_level}

For every question provide:

1. Question
A.
B.
C.
D.

Then provide:

✅ Correct Answer

Keep the quiz educational and clear.
"""

            with st.spinner("🎯 Creating your quiz..."):

                try:

                    answer = ask_gemini(prompt)

                    st.markdown("""
                    <div class="answer-box">
                    <h2 style="color:#312e81;">🎯 Your Practice Quiz</h2>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(answer)

                except Exception as e:

                    st.error("❌ Could not generate quiz.")

                    st.code(str(e))


# ============================================================
# STUDY TOOLS
# ============================================================

st.markdown(
    '<div class="section-title">🛠️ More Study Tools</div>',
    unsafe_allow_html=True
)

tool1, tool2, tool3 = st.columns(3)

with tool1:

    st.markdown("""
    <div class="tip-card">
    <h3 style="color:#1e3a8a;">📄 Study PDF</h3>
    <p style="color:#64748b;">
    Upload your study material and ask questions from it.
    </p>
    </div>
    """, unsafe_allow_html=True)

with tool2:

    st.markdown("""
    <div class="tip-card">
    <h3 style="color:#1e3a8a;">📝 Smart Summary</h3>
    <p style="color:#64748b;">
    Convert long notes into easy revision points.
    </p>
    </div>
    """, unsafe_allow_html=True)

with tool3:

    st.markdown("""
    <div class="tip-card">
    <h3 style="color:#1e3a8a;">📅 Study Planner</h3>
    <p style="color:#64748b;">
    Create a personalized study plan using AI.
    </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# PDF STUDY
# ============================================================

st.markdown(
    '<div class="section-title">📄 Study From Your PDF</div>',
    unsafe_allow_html=True
)

uploaded_pdf = st.file_uploader(
    "📚 Upload your study PDF",
    type=["pdf"]
)

if uploaded_pdf:

    reader = PdfReader(uploaded_pdf)

    pdf_text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            pdf_text += page_text + "\n"

    st.success(
        f"✅ PDF loaded successfully! {len(reader.pages)} page(s) found."
    )

    pdf_question = st.text_area(
        "💭 Ask something about your PDF",
        placeholder="Example: What are the main points of this chapter?"
    )

    if st.button(
        "📚 Ask From PDF",
        use_container_width=True
    ):

        if not pdf_question.strip():

            st.warning("⚠️ Please enter your question.")

        else:

            prompt = f"""
You are an AI Study Assistant.

Answer the student's question using the PDF content.

PDF Content:

{pdf_text[:30000]}

Student Question:

{pdf_question}

Answer in simple language.
Give examples where useful.
"""

            with st.spinner("📚 Reading your PDF..."):

                try:

                    answer = ask_gemini(prompt)

                    st.markdown("""
                    <div class="answer-box">
                    <h2 style="color:#312e81;">📚 PDF Answer</h2>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(answer)

                except Exception as e:

                    st.error("❌ Could not process the PDF.")

                    st.code(str(e))


# ============================================================
# SMART NOTES
# ============================================================

st.markdown(
    '<div class="section-title">📝 Smart Notes Summarizer</div>',
    unsafe_allow_html=True
)

notes = st.text_area(
    "📋 Paste your study notes",
    height=180,
    placeholder="Paste your long study notes here..."
)

if st.button(
    "✨ Summarize My Notes",
    use_container_width=True
):

    if not notes.strip():

        st.warning("⚠️ Please paste some notes first.")

    else:

        prompt = f"""
Summarize these study notes:

{notes}

Give:

📌 Key Concepts

⭐ Important Points

📝 Short Revision Notes

❓ Possible Exam Questions

Use very simple language.
"""

        with st.spinner("📝 Creating your smart notes..."):

            try:

                answer = ask_gemini(prompt)

                st.markdown("""
                <div class="answer-box">
                <h2 style="color:#312e81;">📝 Smart Revision Notes</h2>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(answer)

            except Exception as e:

                st.error("❌ Could not summarize notes.")

                st.code(str(e))


# ============================================================
# STUDY PLANNER
# ============================================================

st.markdown(
    '<div class="section-title">✨ Smart Study Tips</div>',
    unsafe_allow_html=True
)

                

                
                    
                