import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
)

# ---------- DESIGN ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef2ff, #f8fafc);
}

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    color: #172554;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #475569;
    font-size: 20px;
    margin-bottom: 30px;
}

.card {
    padding: 25px;
    border-radius: 20px;
    background: white;
    border: 1px solid #dbeafe;
    box-shadow: 0 8px 25px rgba(30, 64, 175, 0.10);
    text-align: center;
    margin-bottom: 20px;
}

.card:hover {
    transform: translateY(-5px);
    transition: 0.3s;
    box-shadow: 0 12px 30px rgba(30, 64, 175, 0.18);
}

.section-title {
    color: #172554;
    font-size: 30px;
    font-weight: 750;
    margin-top: 20px;
    margin-bottom: 15px;
}

.answer {
    padding: 25px;
    border-radius: 18px;
    background: white;
    border-left: 6px solid #2563eb;
    box-shadow: 0 8px 25px rgba(30, 64, 175, 0.10);
}

.footer {
    text-align: center;
    color: #64748b;
    padding: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown(
    '<div class="main-title">📚 AI Study Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your personal AI tutor 🤖 • Learn • Practice • Revise • Succeed 🚀</div>',
    unsafe_allow_html=True
)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 🎓 Study Center")

    choice = st.radio(
        "Choose a tool:",
        [
            "💬 Ask AI",
            "📖 Explain Topic",
            "📝 Summarize",
            "🎯 Generate Quiz",
            "📅 Study Planner"
        ]
    )

    st.markdown("---")
    st.info("💡 Choose any tool and start learning!")

# ---------- API ----------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    client = None

def ask_ai(prompt):
    if client is None:
        return "🔐 Gemini API key is missing. Add GEMINI_API_KEY in Streamlit Secrets."

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

# ---------- FEATURE CARDS ----------
st.markdown(
    '<div class="section-title">✨ Study Tools</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        '<div class="card"><h2>💬</h2><h3>Ask AI</h3><p>Ask any study question.</p></div>',
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        '<div class="card"><h2>📖</h2><h3>Explain</h3><p>Understand difficult topics.</p></div>',
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        '<div class="card"><h2>📝</h2><h3>Summarize</h3><p>Create quick revision notes.</p></div>',
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        '<div class="card"><h2>🎯</h2><h3>Quiz</h3><p>Practice your knowledge.</p></div>',
        unsafe_allow_html=True
    )

# ---------- ASK AI ----------
if choice == "💬 Ask AI":

    st.markdown(
        '<div class="section-title">💬 Ask Your AI Tutor</div>',
        unsafe_allow_html=True
    )

    question = st.text_area(
        "💭 Your Question",
        placeholder="Example: Explain Python variables in simple language...",
        height=150
    )

    if st.button("🤖 Ask AI", use_container_width=True):

        if not question.strip():
            st.warning("⚠️ Please enter your question first.")

        else:
            with st.spinner("🤖 AI is thinking..."):
                try:
                    answer = ask_ai(
                        f"""
You are a friendly AI Study Assistant.

Answer this student question in very simple language:

{question}

Use this format:

## 📖 Simple Explanation
## 💡 Example
## ⭐ Important Points
## 📝 Quick Revision

Use easy words and helpful emojis.
"""
                    )

                    st.markdown(
                        '<div class="answer"><h2>🤖 AI Tutor Answer</h2></div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(answer)

                except Exception as e:
                    st.error("❌ Something went wrong.")
                    st.code(str(e))

# ---------- EXPLAIN ----------
elif choice == "📖 Explain Topic":

    st.markdown(
        '<div class="section-title">📖 Explain Any Topic</div>',
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "📚 Enter topic",
        placeholder="Example: Recursion in Python"
    )

    level = st.selectbox(
        "🎓 Choose explanation level",
        ["Beginner", "Intermediate", "Exam Level"]
    )

    if st.button("📖 Explain Topic", use_container_width=True):

        if not topic.strip():
            st.warning("⚠️ Enter a topic first.")

        else:
            with st.spinner("📖 Preparing explanation..."):
                try:
                    answer = ask_ai(
                        f"""
Explain {topic} for a {level} student.

Use:
## 📖 Simple Explanation
## 💡 Example
## ⭐ Important Points
## 📝 Quick Revision

Keep it easy to understand.
"""
                    )

                    st.markdown(
                        '<div class="answer"><h2>📖 Topic Explanation</h2></div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(answer)

                except Exception as e:
                    st.error("❌ Could not explain the topic.")
                    st.code(str(e))

# ---------- SUMMARIZE ----------
elif choice == "📝 Summarize":

    st.markdown(
        '<div class="section-title">📝 Smart Summarizer</div>',
        unsafe_allow_html=True
    )

    notes = st.text_area(
        "📄 Paste your notes",
        height=250,
        placeholder="Paste your long study notes here..."
    )

    if st.button("✨ Summarize Notes", use_container_width=True):

        if not notes.strip():
            st.warning("⚠️ Please paste your notes first.")

        else:
            with st.spinner("📝 Creating summary..."):
                try:
                    answer = ask_ai(
                        f"""
Summarize these study notes.

NOTES:
{notes}

Give:

## 📌 Key Concepts
## ⭐ Important Points
## 📝 Revision Notes
## ❓ Possible Exam Questions

Use simple language.
"""
                    )

                    st.markdown(
                        '<div class="answer"><h2>📝 Your Summary</h2></div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(answer)

                except Exception as e:
                    st.error("❌ Could not summarize.")
                    st.code(str(e))

# ---------- QUIZ ----------
elif choice == "🎯 Generate Quiz":

    st.markdown(
        '<div class="section-title">🎯 AI Quiz Generator</div>',
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "📚 Quiz topic",
        placeholder="Example: Python Basics"
    )

    number = st.slider(
        "🔢 Number of questions",
        5,
        15,
        10
    )

    if st.button("🎯 Generate Quiz", use_container_width=True):

        if not topic.strip():
            st.warning("⚠️ Enter a topic first.")

        else:
            with st.spinner("🎯 Creating your quiz..."):
                try:
                    answer = ask_ai(
                        f"""
Create a {number}-question beginner-friendly MCQ quiz about:

{topic}

For every question give:
A.
B.
C.
D.

At the end provide the correct answers.
"""
                    )

                    st.markdown(
                        '<div class="answer"><h2>🎯 Your Quiz</h2></div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(answer)

                except Exception as e:
                    st.error("❌ Could not create quiz.")
                    st.code(str(e))

# ---------- PLANNER ----------
elif choice == "📅 Study Planner":

    st.markdown(
        '<div class="section-title">📅 AI Study Planner</div>',
        unsafe_allow_html=True
    )

    subject = st.text_input(
        "📚 Subject",
        placeholder="Example: Python"
    )

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

    if st.button("🚀 Create Study Plan", use_container_width=True):

        if not subject.strip():
            st.warning("⚠️ Enter a subject first.")

        else:
            with st.spinner("📅 Creating your plan..."):
                try:
                    answer = ask_ai(
                        f"""
Create a realistic study plan.

Subject: {subject}
Days: {days}
Hours per day: {hours}

Give a day-by-day plan with:

📚 Topics
⏰ Study Time
📝 Practice
🔄 Revision

Keep it beginner-friendly.
"""
                    )

                    st.markdown(
                        '<div class="answer"><h2>📅 Your Study Plan</h2></div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(answer)

                except Exception as e:
                    st.error("❌ Could not create study plan.")
                    st.code(str(e))

# ---------- FOOTER ----------
st.markdown("---")

st.markdown(
    """
    <div class="footer">
        <h3>📚 AI Study Assistant 🤖</h3>
        <p>🐍 Python • 🎈 Streamlit • ✨ Gemini AI</p>
        <p>Learn • Practice • Revise • Succeed 🚀</p>
    </div>
    """,
    unsafe_allow_html=True
)