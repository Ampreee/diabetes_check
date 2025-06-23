import requests
import streamlit as st
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import io
import json
import time


def analyse_file(uploaded_file, return_text=False):
    if not uploaded_file:
        return "No file provided.", ""

    file_bytes = uploaded_file.read()
    content_type = uploaded_file.type

    if content_type == "application/pdf":
        pdf_reader = PdfReader(io.BytesIO(file_bytes))
        text = "\n".join(p.extract_text() or "" for p in pdf_reader.pages)
    elif content_type.startswith("image/"):
        image = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(image)
    else:
        text = file_bytes.decode("utf-8", errors="ignore")

    data = {
        "prompt": "What is the likelihood of diabetes for this patient?",
        "context": text,
    }

    api_url = "http://localhost:8000/chat/"
    response = requests.post(api_url, data=data, stream=True)

    def stream_response():
        for line in response.iter_lines():
            if not line:
                continue
            msg = json.loads(line.decode("utf-8"))
            if msg.get("role") == "assistant":
                yield msg["content"] 

    with st.spinner("Analyzing..."):
        placeholder = st.empty()
        full_response = ""
        for chunk in stream_response():
            full_response += chunk
            placeholder.markdown(chunk, unsafe_allow_html=True)  # Only show the latest chunk

    return (full_response, text) if return_text else full_response


def ask_ai(question: str, extracted_text: str, chat_history=None):
    api_url = "http://localhost:8000/chat/"
    data = {
        "prompt": question,
        "context": extracted_text
    }

    with st.spinner("Getting answer..."):
        response = requests.post(api_url, data=data, stream=True)
        full_answer = ""
        placeholder = st.empty()

        for line in response.iter_lines():
            if not line:
                continue
            try:
                msg = json.loads(line)
                if msg["role"] == "assistant":
                    full_answer += msg["content"]
                    placeholder.markdown(full_answer, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error decoding line: {line} - {e}")

    return full_answer
