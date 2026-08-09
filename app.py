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
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #f8f7ff 0%, #eef6ff 50%, #f5f0ff 100%);
}

/* Main content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #17153b 0%, #25205c 50%, #312e81 100%);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.sidebar-title {
    text-align: center;
    font-size: 27px;
    font-weight: 800;
    padding: 15px 5px 20px 5px;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #312e81, #5b21b6, #7c3aed);
    padding: 45px 35px;
    border-radius: 28px;
    text-align: center;
    color: white;
    box-shadow: 0 15px 40px rgba(49, 46, 129, 0.25);
    margin-bottom: 30px;
}

.hero-title {
    font-size: 48px;
    font-weight: 900;
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 21px;
    margin-bottom: 10px;
}

.hero-small {
    font-size: 15px;
    opacity: 0.9;
}

/* Feature cards */
.feature-card {
    background: white;
    padding: 25px 18px;
    border-radius: 20px;
    min-height: 170px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(49, 46, 129, 0.10);
    border: 1px solid #e5e7eb;
    transition: 0.3s;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(49, 46, 129, 0.18);
}

.feature-icon {
    font-size: 42px;
    margin-bottom: 10px;
}

.feature-title {
    font-size: 20px;
    font-weight: 800;
    color: #312e81;
}

.feature-text {
    color: #64748b;
    font-size: 14px;
}

/* Section titles */
.section-title {
    color: #312e81;
    font-size: 30px;
    font-weight: 800;
    margin-top: 30px;
    margin-bottom: 20px;
}

/* Tool box */
.tool-box {
    background: white;
    padding: 30px;
    border-radius: 24px;
    box-shadow: 0 10px 30px rgba(49, 46, 129, 0.10);
    border: 1px solid #e5e7eb;
    margin-top: 20px;
}

/* Answer box */
.answer-box {
    background: linear-gradient(135deg, #eef2ff, #f5f3ff);
    padding: 22px;
    border-radius: 20px;
    border-left: 6px solid #6366f1;
    margin-top: 25px;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: none;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    font-weight: 700;
    padding: 12px 20px;
    transition: 0.25s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(79, 70, 229, 0.3);
}

/* Inputs */
.stTextInput input,
.stTextArea textarea {
    border-radius: 14px !important;
    border: 2px solid #ddd6fe !important;
}

/* Footer */
.footer {
    text-align: center;
    padding: 35px 10px 10px;
    color: #64748b;
}

.footer-title {
    font-size: 22px;
    font-weight: 800;
    color: #312e81;
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

# ============================================================
# GEMINI FUNCTION
# ============================================================

def ask_gemini(prompt):

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-title">
            🎓 Study Center
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🧠 Study Tools")

    selected_tool = st.radio(
        "Choose a tool:",
        [
            "💬 Ask AI",
            "📖 Explain Topic",
            "📝 Summarize Notes",
            "🎯 Generate Quiz",
            "📄 Study PDF",
            "📅 Study Planner"
        ]
    )

    st.markdown("---")

    st.markdown("### 🌟 Features")

    st.markdown(
        """
        📚 Easy explanations

        🤖 AI-powered answers

        💡 Simple language

        📝 Study-friendly notes

        🎯 Exam preparation
        """
    )

    st.markdown("---")

    st.caption(
        "Made with ❤️ using Python + Streamlit + Gemini"
    )

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div style="font-size:55px;">
            📚 🤖 🎓
        </div>

        <div class="hero-title">
            AI Study Assistant
        </div>

        <div class="hero-subtitle">
            Your personal AI tutor 🤖
        </div>

        <div class="hero-small">
            Learn • Practice • Revise • Succeed ✨
        </div>

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
# FEATURE CARDS
# ============================================================

st.markdown(
    '<div class="section-title">✨ What can I help you with?</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(
        """
        <div class="feature-card">

            <div class="feature-icon">💬</div>

            <div class="feature-title">
                Ask AI
            </div>

            <div class="feature-text">
                Ask questions about your subjects.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        """
        <div class="feature-card">

            <div class="feature-icon">📖</div>

            <div class="feature-title">
                Explain
            </div>

            <div class="feature-text">
                Understand difficult concepts easily.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        """
        <div class="feature-card">

            <div class="feature-icon">📝</div>

            <div class="feature-title">
                Summarize
            </div>

            <div class="feature-text">
                Turn long topics into simple notes.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with col4:

    st.markdown(
        """
        <div class="feature-card">

            <div class="feature-icon">🎯</div>

            <div class="feature-title">
                Practice
            </div>

            <div class="feature-text">
                Generate questions for revision.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# ASK AI
# ============================================================

if selected_tool == "💬 Ask AI":

    st.markdown(
        '<div class="section-title">💬 Ask Your AI Tutor</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="tool-box">

        <h3>🤖 I'm ready to help you!</h3>

        <p>
        Ask me anything related to your studies.
        I will explain it in simple language with examples.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    question = st.text_area(
        "💭 Your Question",
        placeholder="Example: Explain Python variables in very simple language...",
        height=150
    )

    if st.button(
        "🤖 Ask AI",
        use_container_width=True
    ):

        if not question.strip():

            st.warning(
                "⚠️ Please enter your question first."
            )

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

            try:

                with st.spinner(
                    "🤖 Your AI tutor is thinking..."
                ):

                    answer = ask_gemini(prompt)

                st.markdown(
                    """
                    <div class="answer-box">

                    <h2>📖 AI Tutor Answer</h2>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(answer)

                st.success(
                    "✅ Done! Keep learning 🚀"
                )

            except Exception as e:

                st.error(
                    "❌ Something went wrong while connecting to Gemini."
                )

                st.code(str(e))

# ============================================================
# EXPLAIN TOPIC
# ============================================================

elif selected_tool == "📖 Explain Topic":

    st.markdown(
        '<div class="section-title">📖 Explain a Topic</div>',
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "📚 Enter your topic",
        placeholder="Example: Explain recursion in Python"
    )

    if st.button(
        "📖 Explain Topic",
        use_container_width=True
    ):

        if not topic.strip():

            st.warning(
                "⚠️ Please enter a topic first."
            )

        else:

            prompt = f"""
Explain the following topic to a beginner:

Topic:
{topic}

Use this structure:

### 📖 Simple Explanation

### 💡 Easy Example

### ⭐ Important Points

### 🧠 Remember This

Use simple language and emojis.
"""

            try:

                with st.spinner(
                    "📖 Preparing a simple explanation..."
                ):

                    answer = ask_gemini(prompt)

                st.markdown(
                    """
                    <div class="answer-box">

                    <h2>📖 Topic Explanation</h2>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(answer)

            except Exception as e:

                st.error(
                    "❌ Could not explain the topic."
                )

                st.code(str(e))

# ============================================================
# SUMMARIZE NOTES
# ============================================================

elif selected_tool == "📝 Summarize Notes":

    st.markdown(
        '<div class="section-title">📝 Smart Notes Summarizer</div>',
        unsafe_allow_html=True
    )

    notes = st.text_area(
        "📄 Paste your study notes here",
        placeholder="Paste your long study notes here...",
        height=250
    )

    if st.button(
        "✨ Summarize Notes",
        use_container_width=True
    ):

        if not notes.strip():

            st.warning(
                "⚠️ Please paste your notes first."
            )

        else:

            prompt = f"""
Summarize the following study notes.

Notes:
{notes}

Give the answer in this structure:

### 📌 Key Concepts

### ⭐ Important Points

### 📝 Short Revision Notes

### ❓ Possible Exam Questions

Use very simple language.
Make it useful for exam revision.
"""

            try:

                with st.spinner(
                    "📝 Creating your summary..."
                ):

                    answer = ask_gemini(prompt)

                st.markdown(
                    """
                    <div class="answer-box">

                    <h2>📝 Your Smart Notes</h2>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(answer)

            except Exception as e:

                st.error(
                    "❌ Could not summarize notes."
                )

                st.code(str(e))

# ============================================================
# QUIZ GENERATOR
# ============================================================

elif selected_tool == "🎯 Generate Quiz":

    st.markdown(
        '<div class="section-title">🎯 AI Quiz Generator</div>',
        unsafe_allow_html=True
    )

    quiz_topic = st.text_input(
        "📚 Enter quiz topic",
        placeholder="Example: Python Basics"
    )

    difficulty = st.selectbox(
        "🎚️ Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    if st.button(
        "🚀 Generate Quiz",
        use_container_width=True
    ):

        if not quiz_topic.strip():

            st.warning(
                "⚠️ Please enter a quiz topic."
            )

        else:

            prompt = f"""
Create a 10-question multiple-choice quiz.

Topic:
{quiz_topic}

Difficulty:
{difficulty}

For every question provide:

1. Question
A.
B.
C.
D.

At the end provide:

### ✅ Correct Answers

Also provide a short explanation for each answer.

Keep the questions educational and clear.
"""

            try:

                with st.spinner(
                    "🎯 Creating your quiz..."
                ):

                    answer = ask_gemini(prompt)

                st.markdown(
                    """
                    <div class="answer-box">

                    <h2>🎯 Your AI Quiz</h2>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(answer)

            except Exception as e:

                st.error(
                    "❌ Could not generate quiz."
                )

                st.code(str(e))

# ============================================================
# PDF STUDY
# ============================================================

elif selected_tool == "📄 Study PDF":

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

                page_text = page.extract_text()

                if page_text:

                    pdf_text += page_text + "\n"

            st.success(
                f"✅ PDF loaded successfully! "
                f"{len(reader.pages)} page(s) found."
            )

            pdf_question = st.text_area(
                "💭 Ask something about your PDF",
                placeholder="Example: What is the main topic of this PDF?"
            )

            if st.button(
                "🤖 Ask PDF",
                use_container_width=True
            ):

                if not pdf_question.strip():

                    st.warning(
                        "⚠️ Please enter your question."
                    )

                else:

                    prompt = f"""
You are an AI Study Assistant.

Use the following PDF content to answer the student's question.

PDF Content:
{pdf_text[:30000]}

Student Question:
{pdf_question}

Answer in very simple language.

If the answer cannot be found in the PDF,
clearly say that the information is not available
in the provided PDF.
"""

                    try:

                        with st.spinner(
                            "📚 Reading your PDF..."
                        ):

                            answer = ask_gemini(prompt)

                        st.markdown(
                            """
                            <div class="answer-box">

                            <h2>📖 PDF Answer</h2>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        st.markdown(answer)

                    except Exception as e:

                        st.error(
                            "❌ Could not answer your PDF question."
                        )

                        st.code(str(e))

        except Exception as e:

            st.error(
                "❌ Could not read this PDF."
            )

            st.code(str(e))

# ============================================================
# STUDY PLANNER
# ============================================================

elif selected_tool == "📅 Study Planner":

    st.markdown(
        '<div class="section-title">📅 Personal Study Planner</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        subject = st.text_input(
            "📚 Subject",
            placeholder="Example: Python"
        )

    with col2:

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

    goal = st.text_input(
        "🎯 Your goal",
        placeholder="Example: Prepare for semester exam"
    )

    if st.button(
        "🚀 Create My Study Plan",
        use_container_width=True
    ):

        if not subject.strip():

            st.warning(
                "⚠️ Please enter a subject."
            )

        else:

            prompt = f"""
Create a realistic study plan for a student.

Subject:
{subject}

Number of days:
{days}

Study hours per day:
{hours}

Student goal:
{goal}

Create a day-by-day study plan.

Include:

📚 Topics
⏰ Suggested study time
📝 Practice
🔄 Revision
🎯 Daily goal

Make the plan beginner-friendly and realistic.
"""

            try:

                with st.spinner(
                    "📅 Creating your personalized plan..."
                ):

                    answer = ask_gemini(prompt)

                st.markdown(
                    """
                    <div class="answer-box">

                    <h2>📅 Your Study Plan</h2>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(answer)

            except Exception as e:

                st.error(
                    "❌ Could not create your study plan."
                )

                st.code(str(e))

# ============================================================
# STUDY TIPS
# ============================================================

st.markdown(
    '<div class="section-title">🌟 Smart Study Tips</div>',
    unsafe_allow_html=True
)

tip1, tip2, tip3 = st.columns(3)

with tip1:

    st.markdown(
        """
        <div class="feature-card">

        <div class="feature-icon">⏰</div>

        <div class="feature-title">
        Study Regularly
        </div>

        <div class="feature-text">
        Study a small amount every day instead
        of studying everything at the last moment.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with tip2:

    st.markdown(
        """
        <div class="feature-card">

        <div class="feature-icon">🧠</div>

        <div class="feature-title">
        Practice More
        </div>

        <div class="feature-text">
        Practice questions regularly to improve
        your understanding and confidence.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with tip3:

    st.markdown(
        """
        <div class="feature-card">

        <div class="feature-icon">🔄</div>

        <div class="feature-title">
        Revise
        </div>

        <div class="feature-text">
        Revise important concepts frequently
        so you can remember them longer.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        <div class="footer-title">
            📚 AI Study Assistant
        </div>

        <p>
            Your personal AI tutor 🤖
        </p>

        <p>
            🐍 Python &nbsp; • &nbsp;
            🎨 Streamlit &nbsp; • &nbsp;
            ✨ Gemini AI
        </p>

        <p>
            💬 Learn &nbsp; • &nbsp;
            📖 Practice &nbsp; • &nbsp;
            🎯 Revise &nbsp; • &nbsp;
            🏆 Succeed
        </p>

    </div>
    """,
    unsafe_allow_html=True
)
