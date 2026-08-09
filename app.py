import streamlit as st
from google import genai
from pypdf import PdfReader

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

    /* Main background */
    .stApp {
        background:
            radial-gradient(circle at top left, #312e81 0%, transparent 30%),
            radial-gradient(circle at bottom right, #581c87 0%, transparent 30%),
            #0f172a;
        color: white;
    }

    /* Main content */
    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Header */
    .hero {
        background: linear-gradient(
            135deg,
            rgba(79,70,229,0.95),
            rgba(124,58,237,0.95)
        );
        padding: 40px 25px;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0 10px 35px rgba(0,0,0,0.35);
        margin-bottom: 30px;
    }

    .hero h1 {
        color: white;
        font-size: 45px;
        margin: 0;
        font-weight: 800;
    }

    .hero p {
        color: #e0e7ff;
        font-size: 20px;
        margin-top: 10px;
    }

    /* Cards */
    .card {
        background: rgba(30,41,59,0.85);
        border: 1px solid rgba(148,163,184,0.25);
        border-radius: 18px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.20);
    }

    .card h3 {
        color: #c4b5fd;
    }

    /* Section title */
    .section-title {
        color: #c4b5fd;
        font-size: 28px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none;
        padding: 12px 20px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white;
        font-size: 16px;
        font-weight: 700;
        transition: 0.3s;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #8b5cf6, #a855f7);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(139,92,246,0.35);
    }

    /* Text areas */
    .stTextArea textarea,
    .stTextInput input {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #6366f1 !important;
        border-radius: 12px !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(30,41,59,0.8);
        border-radius: 15px;
        padding: 10px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #111827,
            #1e1b4b
        );
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #c4b5fd;
    }

    /* Info boxes */
    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid #334155;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# GEMINI API
# ============================================================

if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ Gemini API key is missing.")
    st.info("Go to Streamlit → Manage app → Settings → Secrets.")
    st.stop()

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


# ============================================================
# HERO HEADER
# ============================================================

st.markdown("""
<div class="hero">

    <h1>📚 AI Study Assistant</h1>

    <p>
        Your personal AI tutor 🤖
        <br>
        Learn • Practice • Revise • Succeed 🚀
    </p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🎓 Study Center")

    st.write("Choose what you want to do:")

    tool = st.radio(
        "Study Tools",
        [
            "💬 Ask AI",
            "📄 Ask from PDF",
            "📖 Explain Topic",
            "📝 Summarize Notes",
            "🎯 Generate Quiz",
            "📅 Study Planner"
        ]
    )

    st.divider()

    st.markdown("### 💡 Study Tip")

    st.info(
        "Study a little every day instead of trying to learn "
        "everything at the last moment."
    )

    st.divider()

    st.caption("🐍 Python + Streamlit + Gemini")


# ============================================================
# ASK AI
# ============================================================

if tool == "💬 Ask AI":

    st.markdown(
        '<div class="section-title">💬 Ask Your AI Tutor</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="card">
        <h3>🤖 Ask me anything about your studies!</h3>
        <p>
        Get simple explanations, examples and important points.
        </p>
    </div>
    """, unsafe_allow_html=True)

    question = st.text_area(
        "💭 Your Question",
        placeholder="Example: Explain Python variables in simple language.",
        height=150
    )

    if st.button("🤖 Ask AI"):

        if not question.strip():

            st.warning("⚠️ Please enter a question.")

        else:

            with st.spinner("🤖 AI is thinking..."):

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=f"""
                    You are a friendly AI Study Assistant.

                    Answer the student's question in very simple,
                    beginner-friendly language.

                    Question:
                    {question}

                    Give:
                    1. Simple Explanation
                    2. Example
                    3. Important Points
                    4. Short Summary
                    """
                )

            st.markdown("### 📖 AI Answer")

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            st.write(response.text)

            st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# ASK FROM PDF
# ============================================================

elif tool == "📄 Ask from PDF":

    st.markdown(
        '<div class="section-title">📄 Study From Your PDF</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Upload your notes or textbook PDF and ask questions from it."
    )

    uploaded_file = st.file_uploader(
        "📎 Upload your study PDF",
        type=["pdf"]
    )

    if uploaded_file:

        st.success(
            f"✅ {uploaded_file.name} uploaded successfully!"
        )

        reader = PdfReader(uploaded_file)

        pdf_text = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pdf_text += text + "\n"

        st.info(
            f"📄 Total pages: {len(reader.pages)}"
        )

        question = st.text_area(
            "💭 Ask something about your PDF",
            placeholder="Example: Explain the important points of this chapter.",
            height=130
        )

        if st.button("🔍 Ask From PDF"):

            if not question.strip():

                st.warning("⚠️ Please enter a question.")

            elif not pdf_text.strip():

                st.error(
                    "❌ Could not extract text from this PDF."
                )

            else:

                with st.spinner("📚 Reading your study material..."):

                    context = pdf_text[:50000]

                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=f"""
                        You are an AI Study Assistant.

                        Use the study material below to answer
                        the student's question.

                        STUDY MATERIAL:

                        {context}

                        STUDENT QUESTION:

                        {question}

                        Instructions:
                        - Use simple language.
                        - Give a clear answer.
                        - Use examples when useful.
                        - If the answer is not present in the PDF,
                          clearly say so.
                        """
                    )

                st.markdown("### 📖 Answer")

                st.markdown(
                    '<div class="card">',
                    unsafe_allow_html=True
                )

                st.write(response.text)

                st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# EXPLAIN TOPIC
# ============================================================

elif tool == "📖 Explain Topic":

    st.markdown(
        '<div class="section-title">📖 Topic Explainer</div>',
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "📚 Enter a topic",
        placeholder="Example: Python Functions"
    )

    if st.button("✨ Explain Topic"):

        if not topic.strip():

            st.warning("⚠️ Please enter a topic.")

        else:

            with st.spinner("📖 Preparing explanation..."):

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=f"""
                    Explain {topic} to a beginner.

                    Include:

                    1. Definition
                    2. Simple explanation
                    3. Real-life example
                    4. Programming/example if relevant
                    5. Important points
                    6. Short summary
                    """
                )

            st.markdown("### 📚 Explanation")

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            st.write(response.text)

            st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# SUMMARIZE NOTES
# ============================================================

elif tool == "📝 Summarize Notes":

    st.markdown(
        '<div class="section-title">📝 Smart Notes Summarizer</div>',
        unsafe_allow_html=True
    )

    notes = st.text_area(
        "📚 Paste your notes here",
        placeholder="Paste your chapter notes...",
        height=250
    )

    if st.button("📝 Summarize Notes"):

        if not notes.strip():

            st.warning("⚠️ Please paste your notes.")

        else:

            with st.spinner("🧠 Creating your summary..."):

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=f"""
                    Summarize the following study notes.

                    NOTES:

                    {notes}

                    Give:

                    📌 Important Points
                    📖 Key Definitions
                    🎯 Exam-Focused Points
                    🧠 Easy Revision Notes
                    """
                )

            st.markdown("### 📋 Your Summary")

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            st.write(response.text)

            st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# QUIZ GENERATOR
# ============================================================

elif tool == "🎯 Generate Quiz":

    st.markdown(
        '<div class="section-title">🎯 AI Quiz Generator</div>',
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "📚 Quiz Topic",
        placeholder="Example: Python Basics"
    )

    number = st.slider(
        "Number of Questions",
        min_value=5,
        max_value=20,
        value=10
    )

    if st.button("🎯 Generate Quiz"):

        if not topic.strip():

            st.warning("⚠️ Please enter a topic.")

        else:

            with st.spinner("🎯 Creating your quiz..."):

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=f"""
                    Create {number} MCQ questions about {topic}.

                    For every question provide:

                    Question
                    A. Option
                    B. Option
                    C. Option
                    D. Option

                    Correct Answer
                    Short Explanation

                    Make the questions suitable for students.
                    """
                )

            st.markdown("### 🎯 Your Quiz")

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            st.write(response.text)

            st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# STUDY PLANNER
# ============================================================

elif tool == "📅 Study Planner":

    st.markdown(
        '<div class="section-title">📅 AI Study Planner</div>',
        unsafe_allow_html=True
    )

    subject = st.text_input(
        "📚 Subject",
        placeholder="Example: Python Programming"
    )

    col1, col2 = st.columns(2)

    with col1:

        days = st.number_input(
            "📅 Number of Days",
            min_value=1,
            max_value=60,
            value=7
        )

    with col2:

        hours = st.number_input(
            "⏰ Hours Per Day",
            min_value=1,
            max_value=12,
            value=2
        )

    if st.button("📅 Create My Study Plan"):

        if not subject.strip():

            st.warning("⚠️ Please enter a subject.")

        else:

            with st.spinner("📅 Creating your study plan..."):

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=f"""
                    Create a {days}-day study plan for:

                    Subject: {subject}

                    Study time:
                    {hours} hours per day.

                    Include:

                    Day-by-day topics
                    Study time
                    Practice
                    Revision
                    Quiz/Test
                    Final revision
                    """
                )

            st.markdown("### 📅 Your Personalized Plan")

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            st.write(response.text)

            st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

    <b>📚 AI Study Assistant</b>

    <br><br>

    Made with ❤️ using Python 🐍 + Streamlit 🎈 + Gemini 🤖

    <br>

    Learn • Practice • Revise • Succeed 🚀

</div>
""", unsafe_allow_html=True)
