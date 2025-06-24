import requests
import streamlit as st
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import io
import json

def analyse_file(uploaded_file):
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

    data = {"context": text}
    api_url = "http://backend:8000/analyze/"
    response = requests.post(api_url, data=data, stream=True)

    def stream_response():
        for line in response.iter_lines():
            if not line:
                continue
            try:
                msg = json.loads(line.decode("utf-8"))
                if msg.get("role") == "assistant":
                    yield msg["content"]
            except Exception as e:
                yield f"Error decoding line: {line} - {e}"

    with st.spinner("Analyzing..."):
        placeholder = st.empty()
        result = ""
        for chunk in stream_response():
            result = chunk
            placeholder.markdown(chunk, unsafe_allow_html=True)
    return result, text

def ask_ai(question: str, analysis: str, context: str):
    api_url = "http://backend:8000/ask/"
    data = {
        "question": question,
        "analysis": analysis,
        "context": context
    }
    response = requests.post(api_url, data=data, stream=True)
    def stream_response():
        for line in response.iter_lines():
            if not line:
                continue
            try:
                msg = json.loads(line.decode("utf-8"))
                if msg.get("role") == "assistant":
                    yield msg["content"]
            except Exception as e:
                yield f"Error decoding line: {line} - {e}"

    with st.spinner("Getting answer..."):
        placeholder = st.empty()
        answer = ""
        for chunk in stream_response():
            answer = chunk
            placeholder.markdown(chunk, unsafe_allow_html=True)
    return answer