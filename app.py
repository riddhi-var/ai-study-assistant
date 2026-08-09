import streamlit as st
from google import genai
from pypdf import PdfReader

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Study Assistant")
st.write("Your personal AI tutor 🤖")

# -----------------------------
# Gemini API
# -----------------------------

if "GEMINI_API_KEY" not in st.secrets:
    st.error("GEMINI_API_KEY is missing from Streamlit Secrets.")
    st.stop()

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("🎓 Study Tools")

tool = st.sidebar.selectbox(
    "Choose a tool",
    [
        "💬 Ask a Question",
        "📄 Ask from PDF",
        "📚 Explain a Topic",
        "📝 Summarize Notes",
        "🎯 Generate Quiz",
        "📅 Create Study Plan"
    ]
)

# -----------------------------
# Ask General Question
# -----------------------------

if tool == "💬 Ask a Question":

    st.header("💬 Ask a Question")

    question = st.text_area(
        "Enter your question",
        placeholder="Example: Explain Python variables in simple language."
    )

    if st.button("🤖 Ask AI"):

        if not question.strip():
            st.warning("Please enter a question.")

        else:

            with st.spinner("AI is thinking..."):

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=f"""
                    You are a helpful AI Study Assistant.

                    Explain the following question in simple
                    beginner-friendly language.

                    Question:
                    {question}

                    Include:
                    1. Simple explanation
                    2. Example
                    3. Important points
                    """
                )

            st.subheader("📖 Answer")
            st.write(response.text)


# -----------------------------
# PDF Question Answering
# -----------------------------

elif tool == "📄 Ask from PDF":

    st.header("📄 Ask Questions from Your PDF")

    st.info(
        "Upload your study notes or textbook PDF and ask questions about it."
    )

    uploaded_file = st.file_uploader(
        "📎 Upload PDF",
        type=["pdf"]
    )

    if uploaded_file:

        st.success(f"Uploaded: {uploaded_file.name}")

        reader = PdfReader(uploaded_file)

        pdf_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pdf_text += text + "\n"

        st.write(f"📄 Pages: {len(reader.pages)}")

        question = st.text_area(
            "💬 Ask a question about your PDF",
            placeholder="Example: What is the main topic of this chapter?"
        )

        if st.button("🔍 Ask from PDF"):

            if not question.strip():

                st.warning("Please enter a question.")

            elif not pdf_text.strip():

                st.error(
                    "I couldn't extract text from this PDF. "
                    "Try a text-based PDF."
                )

            else:

                with st.spinner("Reading your notes..."):

                    # Limit text to avoid sending an extremely
                    # large document to the model.
                    context = pdf_text[:50000]

                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=f"""
                        You are an AI Study Assistant.

                        Answer the student's question using the
                        uploaded study material below.

                        STUDY MATERIAL:
                        {context}

                        STUDENT QUESTION:
                        {question}

                        Instructions:
                        - Answer in simple language.
                        - Use only information from the study material
                          when possible.
                        - If the answer is not present in the material,
                          clearly say that.
                        - Give examples when useful.
                        """
                    )

                st.subheader("📖 Answer from Your PDF")
                st.write(response.text)


# -----------------------------
# Explain Topic
# -----------------------------

elif tool == "📚 Explain a Topic":

    st.header("📚 Explain a Topic")

    topic = st.text_input(
        "Enter topic",
        placeholder="Example: Python Functions"
    )

    if st.button("✨ Explain"):

        if topic:

            with st.spinner("Preparing explanation..."):

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=f"""
                    Explain {topic} to a beginner.

                    Include:
                    - Definition
                    - Simple explanation
                    - Example
                    - Important points
                    - Short summary
                    """
                )

            st.subheader("📖 Explanation")
            st.write(response.text)

        else:
            st.warning("Please enter a topic.")


# -----------------------------
# Summarize Notes
# -----------------------------

elif tool == "📝 Summarize Notes":

    st.header("📝 Summarize Notes")

    notes = st.text_area(
        "Paste your study notes",
        height=250
    )

    if st.button("📝 Summarize"):

        if notes:

            with st.spinner("Summarizing..."):

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=f"""
                    Summarize these study notes.

                    NOTES:
                    {notes}

                    Give:
                    - Important points
                    - Key definitions
                    - Exam-focused points
                    - Short revision summary
                    """
                )

            st.subheader("📋 Summary")
            st.write(response.text)

        else:
            st.warning("Please paste some notes.")


# -----------------------------
# Generate Quiz
# -----------------------------

elif tool == "🎯 Generate Quiz":

    st.header("🎯 Generate MCQ Quiz")

    topic = st.text_input(
        "Enter quiz topic",
        placeholder="Example: Python Basics"
    )

    number = st.slider(
        "Number of questions",
        5,
        20,
        10
    )

    if st.button("🎯 Generate Quiz"):

        if topic:

            with st.spinner("Creating quiz..."):

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=f"""
                    Create {number} multiple-choice questions
                    about {topic}.

                    For every question provide:
                    - Question
                    - Four options
                    - Correct answer
                    - Short explanation
                    """
                )

            st.subheader("🎯 Quiz")
            st.write(response.text)

        else:
            st.warning("Please enter a topic.")


# -----------------------------
# Study Plan
# -----------------------------

elif tool == "📅 Create Study Plan":

    st.header("📅 Create Study Plan")

    subject = st.text_input(
        "Subject",
        placeholder="Example: Python Programming"
    )

    days = st.number_input(
        "Number of days",
        min_value=1,
        max_value=30,
        value=7
    )

    hours = st.number_input(
        "Study hours per day",
        min_value=1,
        max_value=12,
        value=2
    )

    if st.button("📅 Create Plan"):

        if subject:

            with st.spinner("Creating study plan..."):

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=f"""
                    Create a {days}-day study plan for {subject}.

                    The student can study {hours} hours per day.

                    Include:
                    - Daily topics
                    - Study time
                    - Practice
                    - Revision
                    - Quiz/test
                    """
                )

            st.subheader("📅 Your Study Plan")
            st.write(response.text)

        else:
            st.warning("Please enter a subject.")


st.divider()

st.caption("Made with Python 🐍 + Streamlit + Gemini 🤖")
