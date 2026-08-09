import streamlit as st

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚"
)

st.title("📚 AI Study Assistant")

st.write("🎉 Your Streamlit app is working!")

name = st.text_input("Enter your name")

if st.button("Start Studying"):
    if name:
        st.success(f"Welcome, {name}! Let's start studying 🚀")
    else:
        st.warning("Please enter your name.")
