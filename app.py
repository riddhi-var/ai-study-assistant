import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚"
)

st.title("📚 AI Study Assistant")
st.write("Your personal AI tutor 🤖")

# Get Gemini API key
if "GEMINI_API_KEY" not in st.secrets:
    st.error("GEMINI_API_KEY is missing from Streamlit Secrets.")
    st.stop()

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# Sidebar
st.sidebar.title("🎓 Study Tools")

tool = st.sidebar.selectbox(
    "Choose a tool",
    [
        "Ask a Question",
        "Explain a Topic",
        "Summarize Notes",
        "Generate Quiz",
        "Create Study Plan"
    ]
)

# Ask Question
if tool == "Ask a Question":

    question = st.text_area(
        "💬 Ask your question",
        placeholder="Example: What is a Python variable?"
    )

    if st.button("🤖 Ask AI"):

        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("AI is thinking..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"""
                    You are a helpful AI Study Assistant.

                    Answer the student's question in very simple language.

                    Question:
                    {question}

                    Give:
                    1. Simple explanation
                    2. Example
                    3. Important points
                    """
                )

            st.subheader("📖 Answer")
            st.write(response.text)


# Explain Topic
elif tool == "Explain a Topic":

    topic = st.text_input(
        "📚 Enter topic",
        placeholder="Example: Python Functions"
    )

    if st.button("✨ Explain"):

        if topic:

            with st.spinner("Preparing explanation..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
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


# Summarize Notes
elif tool == "Summarize Notes":

    notes = st.text_area(
        "📝 Paste your notes",
        height=250
    )

    if st.button("📝 Summarize"):

        if notes:

            with st.spinner("Summarizing..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"""
                    Summarize these study notes.

                    Notes:
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


# Generate Quiz
elif tool == "Generate Quiz":

    topic = st.text_input(
        "❓ Enter quiz topic",
        placeholder="Example: Data Structures"
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
                    model="gemini-2.5-flash",
                    contents=f"""
                    Create {number} MCQs about {topic}.

                    For every question provide:
                    - Question
                    - 4 options
                    - Correct answer
                    - Short explanation
                    """
                )

            st.subheader("🎯 Quiz")
            st.write(response.text)


# Study Plan
elif tool == "Create Study Plan":

    subject = st.text_input(
        "📚 Subject",
        placeholder="Example: Python Programming"
    )

    days = st.number_input(
        "Number of days",
        min_value=1,
        max_value=30,
        value=7
    )

    if st.button("📅 Create Plan"):

        if subject:

            with st.spinner("Creating study plan..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"""
                    Create a {days}-day study plan for {subject}.

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

st.divider()

st.caption("Made with Python 🐍 + Streamlit + Gemini 🤖")
