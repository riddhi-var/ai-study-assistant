import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚"
)

st.title("📚 AI Study Assistant")
st.write("Ask me any study question!")

# Check whether the secret exists
if "OPENAI_API_KEY" not in st.secrets:
    st.error("OPENAI_API_KEY is missing from Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

question = st.text_area(
    "💬 Your question",
    placeholder="Example: Explain Python loops in simple language."
)

if st.button("🤖 Ask AI"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("AI is thinking..."):
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    input=f"""
                    You are a helpful AI Study Assistant.

                    Explain this question in simple language:
                    {question}

                    Give an easy explanation and an example.
                    """
                )

            st.subheader("📖 Answer")
            st.write(response.output_text)

        except Exception as e:
            st.error("There was a problem connecting to the AI.")
            st.code(str(e))
