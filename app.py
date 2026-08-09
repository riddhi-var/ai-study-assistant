import streamlit as st
from google import genai
from pypdf import PdfReader

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM DESIGN
# =========================================================

st.markdown("""
<style>

    /* ---------- MAIN PAGE ---------- */

    .stApp {
        background: #f4f8fc;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 30px;
        padding-bottom: 50px;
    }

    /* ---------- HEADER ---------- */

    .hero {
        background: linear-gradient(
            135deg,
            #0f4c81,
            #147d92
        );

        padding: 38px 30px;
        border-radius: 22px;
        text-align: center;

        box-shadow:
            0 8px 25px rgba(15, 76, 129, 0.20);

        margin-bottom: 30px;
    }

    .hero h1 {
        color: white !important;
        font-size: 44px;
        font-weight: 800;
        margin: 0;
        letter-spacing: 0.5px;
    }

    .hero p {
        color: #e8f7fa !important;
        font-size: 19px;
        margin-top: 12px;
        line-height: 1.6;
    }

    /* ---------- SECTION TITLE ---------- */

    .section-title {
        color: #123b5d;
        font-size: 30px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 18px;
    }

    /* ---------- CARDS ---------- */

    .card {
        background: white;
        border: 1px solid #dbe7f0;
        border-radius: 18px;
        padding: 25px;

        box-shadow:
            0 5px 18px rgba(20, 55, 80, 0.08);

        margin-bottom: 20px;
    }

    .card h3 {
        color: #0f4c81;
        margin-top: 0;
    }

    .card p {
        color: #526579;
        font-size: 16px;
    }

    /* ---------- SIDEBAR ---------- */

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #d9e5ee;
    }

    [data-testid="stSidebar"] * {
        color: #173b57 !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #0f4c81 !important;
    }

    /* Sidebar radio buttons */

    [data-testid="stSidebar"] .stRadio label {
        font-weight: 600;
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        width: 100%;

        background: #147d92;
        color: white !important;

        border: none;
        border-radius: 10px;

        padding: 12px 20px;

        font-size: 16px;
        font-weight: 700;

        transition: 0.2s;
    }

    .stButton > button:hover {
        background: #0f6477;
        color: white !important;

        transform: translateY(-2px);

        box-shadow:
            0 6px 15px rgba(20, 125, 146, 0.25);
    }

    /* ---------- INPUTS ---------- */

    .stTextInput input,
    .stTextArea textarea {

        background: white !important;

        color: #173b57 !important;

        border: 1px solid #cbdce8 !important;

        border-radius: 10px !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {

        border: 2px solid #147d92 !important;
    }

    /* ---------- FILE UPLOADER ---------- */

    [data-testid="stFileUploader"] {

        background: white;

        border: 1px dashed #9dbccc;

        border-radius: 15px;

        padding: 12px;
    }

    /* ---------- SELECT BOX ---------- */

    div[data-baseweb="select"] > div {

        background-color: white !important;

        border-radius: 10px !important;

        border-color: #cbdce8 !important;
    }

    /* ---------- FOOTER ---------- */

    .footer {

        text-align: center;

        color: #6d8192;

        margin-top: 50px;

        padding: 25px;

        border-top: 1px solid #d9e5ee;
    }

    /* ---------- INFO BOX ---------- */

    [data-testid="stAlert"] {

        border-radius: 12px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# GEMINI API
# =========================================================

if "GEMINI_API_KEY" not in st.secrets:

    st.error("❌ Gemini API key is missing.")

    st.info(
        "Go to Streamlit → Manage app → Settings → Secrets "
        "and add GEMINI_API_KEY."
    )

    st.stop()


client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


# =========================================================
# HEADER
# =========================================================

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


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 📚 Study Assistant")

    st.write("Choose a tool:")

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
        "Small daily study sessions are better "
        "than last-minute preparation."
    )

    st.divider()

    st.markdown("### 🛠️ Technology")

    st.write("🐍 Python")
    st.write("🎈 Streamlit")
    st.write("🤖 Gemini AI")

    st.divider()

    st.caption("Made for students ❤️")


# =========================================================
# ASK AI
# =========================================================

if tool == "💬 Ask AI":

    st.markdown(
        '<div class="section-title">💬 Ask Your AI Tutor</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="card">

        <h3>🤖 What would you like to learn?</h3>

        <p>
            Ask questions about programming, mathematics,
            science, engineering or any other subject.
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

                try:

                    response = client.models.generate_content(

                        model="gemini-3.5-flash-lite",

                        contents=f"""
You are a friendly AI Study Assistant.

Answer the student's question using very simple,
beginner-friendly language.

Question:
{question}

Give the answer using:

1. 📖 Simple Explanation
2. 💡 Example
3. ⭐ Important Points
4. 📝 Short Summary
"""
                    )

                    st.markdown("### 📖 AI Answer")

                    st.markdown(
                        '<div class="card">',
                        unsafe_allow_html=True
                    )

                    st.write(response.text)

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

                except Exception as e:

                    st.error("❌ Something went wrong.")

                    st.code(str(e))


# =========================================================
# ASK FROM PDF
# =========================================================

elif tool == "📄 Ask from PDF":

    st.markdown(
        '<div class="section-title">📄 Study From Your PDF</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="card">

        <h3>📚 Upload Your Study Material</h3>

        <p>
            Upload your PDF notes or textbook and ask
            questions directly from your material.
        </p>

    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "📎 Upload PDF",
        type=["pdf"]
    )

    if uploaded_file:

        st.success(
            f"✅ {uploaded_file.name} uploaded!"
        )

        reader = PdfReader(uploaded_file)

        pdf_text = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:

                pdf_text += text + "\n"

        st.info(
            f"📄 Pages found: {len(reader.pages)}"
        )

        question = st.text_area(
            "💭 Ask a question from this PDF",
            placeholder="Example: What are the important points?",
            height=130
        )

        if st.button("🔍 Ask From PDF"):

            if not question.strip():

                st.warning("⚠️ Enter a question.")

            elif not pdf_text.strip():

                st.error(
                    "❌ No readable text found in this PDF."
                )

            else:

                with st.spinner(
                    "📚 Reading your study material..."
                ):

                    try:

                        response = client.models.generate_content(

                            model="gemini-3.5-flash-lite",

                            contents=f"""
You are an AI Study Assistant.

Use the following study material to answer
the student's question.

STUDY MATERIAL:

{pdf_text[:50000]}

QUESTION:

{question}

Use simple language and examples.

If the answer is not found in the material,
clearly tell the student.
"""
                        )

                        st.markdown("### 📖 Answer")

                        st.markdown(
                            '<div class="card">',
                            unsafe_allow_html=True
                        )

                        st.write(response.text)

                        st.markdown(
                            "</div>",
                            unsafe_allow_html=True
                        )

                    except Exception as e:

                        st.error("❌ AI error.")

                        st.code(str(e))


# =========================================================
# EXPLAIN TOPIC
# =========================================================

elif tool == "📖 Explain Topic":

    st.markdown(
        '<div class="section-title">📖 Topic Explainer</div>',
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "📚 Enter Topic",
        placeholder="Example: Python Functions"
    )

    if st.button("✨ Explain Topic"):

        if not topic.strip():

            st.warning("⚠️ Enter a topic first.")

        else:

            with st.spinner(
                "📖 Preparing your explanation..."
            ):

                try:

                    response = client.models.generate_content(

                        model="gemini-3.5-flash-lite",

                        contents=f"""
Explain {topic} to a beginner.

Include:

1. Definition
2. Simple Explanation
3. Real-Life Example
4. Example/Code if relevant
5. Important Points
6. Short Summary
"""
                    )

                    st.markdown("### 📚 Explanation")

                    st.markdown(
                        '<div class="card">',
                        unsafe_allow_html=True
                    )

                    st.write(response.text)

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

                except Exception as e:

                    st.error("❌ AI error.")

                    st.code(str(e))


# =========================================================
# SUMMARIZE NOTES
# =========================================================

elif tool == "📝 Summarize Notes":

    st.markdown(
        '<div class="section-title">📝 Smart Notes Summarizer</div>',
        unsafe_allow_html=True
    )

    notes = st.text_area(
        "📚 Paste Your Notes",
        placeholder="Paste your chapter notes here...",
        height=250
    )

    if st.button("📝 Summarize Notes"):

        if not notes.strip():

            st.warning("⚠️ Paste your notes first.")

        else:

            with st.spinner(
                "🧠 Creating your summary..."
            ):

                try:

                    response = client.models.generate_content(

                        model="gemini-3.5-flash-lite",

                        contents=f"""
Summarize these study notes.

NOTES:

{notes}

Create:

📌 Important Points

📖 Key Definitions

🎯 Exam-Focused Points

🧠 Easy Revision Notes
"""
                    )

                    st.markdown("### 📋 Summary")

                    st.markdown(
                        '<div class="card">',
                        unsafe_allow_html=True
                    )

                    st.write(response.text)

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

                except Exception as e:

                    st.error("❌ AI error.")

                    st.code(str(e))


# =========================================================
# QUIZ GENERATOR
# =========================================================

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
        5,
        20,
        10
    )

    if st.button("🎯 Generate Quiz"):

        if not topic.strip():

            st.warning("⚠️ Enter a topic.")

        else:

            with st.spinner(
                "🎯 Creating your quiz..."
            ):

                try:

                    response = client.models.generate_content(

                        model="gemini-3.5-flash-lite",

                        contents=f"""
Create {number} multiple-choice questions
about {topic}.

For every question provide:

Question

A. Option

B. Option

C. Option

D. Option

Correct Answer

Short Explanation

Make the quiz suitable for students.
"""
                    )

                    st.markdown("### 🎯 Your Quiz")

                    st.markdown(
                        '<div class="card">',
                        unsafe_allow_html=True
                    )

                    st.write(response.text)

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

                except Exception as e:

                    st.error("❌ AI error.")

                    st.code(str(e))


# =========================================================
# STUDY PLANNER
# =========================================================

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

            st.warning("⚠️ Enter a subject.")

        else:

            with st.spinner(
                "📅 Creating your study plan..."
            ):

                try:

                    response = client.models.generate_content(

                        model="gemini-3.5-flash-lite",

                        contents=f"""
Create a {days}-day study plan.

Subject:
{subject}

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

                    st.markdown(
                        "### 📅 Your Personalized Study Plan"
                    )

                    st.markdown(
                        '<div class="card">',
                        unsafe_allow_html=True
                    )

                    st.write(response.text)

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

                except Exception as e:

                    st.error("❌ AI error.")

                    st.code(str(e))


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

    <b>📚 AI Study Assistant</b>

    <br><br>

    Your personal AI tutor 🤖

    <br><br>

    Built with 🐍 Python
    • 🎈 Streamlit
    • 🤖 Gemini AI

    <br><br>

    <b>Learn • Practice • Revise • Succeed 🚀</b>

</div>
""", unsafe_allow_html=True)
