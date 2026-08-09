import streamlit as st
from google import genai
from pypdf import PdfReader

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
)

# 🎨 Custom Styling
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #eef2ff, #f0fdf4);
}

h1 {
    color: #4f46e5;
    text-align: center;
    font-size: 42px;
}

h2, h3 {
    color: #3730a3;
}

.stButton > button {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 25px;
    font-weight: bold;
}

[data-testid="stSidebar"] {
    background: #eef2ff;
}

</style>
""", unsafe_allow_html=True)

st.title("📚 AI Study Assistant")
st.write("Your personal AI tutor 🤖")
