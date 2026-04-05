import streamlit as st
import PyPDF2
import os
import requests
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="AI Work Assistant", layout="centered")
st.title("🚀 AI Work Assistant")
st.write("Automate tasks like summarization, email writing, and data extraction using AI.")

# Input
st.subheader("📥 Input Section")
user_input = st.text_area("Enter your text")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

text = ""

# PDF extraction
if uploaded_file:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

# Combine
final_input = user_input + "\n" + text

# Task selection
task = st.selectbox("Choose Task", ["Summarize", "Extract Key Points", "Write Email"])

# --- FIXED: Only ONE Run button ---
if st.button("Run AI"):
    if final_input.strip() == "":
        st.warning("Please enter text or upload file")
    else:
        # Prompt creation
        if task == "Summarize":
            prompt = f"Summarize the following content:\n{final_input}"
        elif task == "Extract Key Points":
            prompt = f"Extract key points in bullet format:\n{final_input}"
        else:
            prompt = f"Write a professional email based on:\n{final_input}"

        # API call
        with st.spinner("Processing..."):
         # ✅ Fixed URL using the current standard model
            # ✅ Fixed URL using the current Gemini 2.5 Flash model
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
            headers = {
                "Content-Type": "application/json"
            }

            data = {
                "contents": [
                    {
                        "parts": [{"text": prompt}]
                    }
                ]
            }

            response = requests.post(url, headers=headers, json=data)
            result = response.json()

        # SAFE output handling
        st.subheader("📤 Output Section")

        if "candidates" in result:
            output = result['candidates'][0]['content']['parts'][0]['text']
            st.write(output)
        else:
            st.error("API Error:")
            st.write(result)