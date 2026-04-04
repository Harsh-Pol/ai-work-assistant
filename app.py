import streamlit as st
import google.generativeai as genai
import PyPDF2
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

st.set_page_config(page_title="AI Work Assistant", layout="centered")
st.title("🚀 AI Work Assistant")
st.write("Automate tasks like summarization, email writing, and data extraction using AI.")

# Input text
st.subheader("📥 Input Section")
user_input = st.text_area("Enter your text")

# File upload
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

text = ""

# Extract text from PDF
if uploaded_file:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        text += page.extract_text()

# Combine input
final_input = user_input + "\n" + text

# Task selection
task = st.selectbox("Choose Task", ["Summarize", "Extract Key Points", "Write Email"])

# Run AI
if st.button("Run AI"):
    if final_input.strip() == "":
        st.warning("Please enter text or upload file")
    else:
        if task == "Summarize":
            prompt = f"Summarize the following content in a clear and concise way:\n{final_input}"
        elif task == "Extract Key Points":
            prompt = f"Extract the most important key points in bullet format:\n{final_input}"
else:
    prompt = f"Write a professional and clear email based on this content:\n{final_input}"

    with st.spinner("Processing..."):
        response = model.generate_content(prompt)
    st.subheader("📤 Output Section")
    st.subheader("Output:")
    st.write(response.text)