from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, AsyncGenerator
from pydantic_ai import Agent
from pydantic_ai.messages import TextPart,ModelResponse
from datetime import datetime, timezone
import json
import io
from src.prompts import p1,p2
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = Agent('openai:gpt-4o')

def extract_text_from_file(uploaded_file: UploadFile) -> str:
    file_type = uploaded_file.content_type
    content = uploaded_file.file.read()
    if file_type == "application/pdf":
        reader = PdfReader(io.BytesIO(content))
        return "\n".join(p.extract_text() or "" for p in reader.pages)
    elif file_type.startswith("image/"):
        image = Image.open(io.BytesIO(content))
        return pytesseract.image_to_string(image)
    else:
        return content.decode("utf-8", errors="ignore")

@app.post("/analyze/")
async def analyze_file(context: str = Form(...)):
    full_prompt = f"""
{p1}

. Given the following patient data:

{context}

Provide a medical summary and risk assessment for diabetes.
"""
    async def stream_messages() -> AsyncGenerator[bytes, None]:
        yield json.dumps({
            "role": "user",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "content": "Analyze uploaded patient data."
        }).encode("utf-8") + b"\n"

        async with agent.run_stream(full_prompt) as result:
            async for delta in result.stream(debounce_by=0.05):
                yield json.dumps({
                    "role": "assistant",
                    "timestamp": result.timestamp().isoformat(),
                    "content": delta
                }).encode("utf-8") + b"\n"
    return StreamingResponse(stream_messages(), media_type="text/plain")

@app.post("/ask/")
async def ask_ai(
    question: str = Form(...),
    analysis: str = Form(...),
    context: str = Form(...)
):
    full_prompt = f"""
{p2}

Here is the initial analysis of the file:

{analysis}

Here is the original patient data:

{context}

Answer the user's follow-up question: {question}
"""
    async def stream_messages() -> AsyncGenerator[bytes, None]:
        yield json.dumps({
            "role": "user",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "content": question
        }).encode("utf-8") + b"\n"
        async with agent.run_stream(full_prompt) as result:
            async for delta in result.stream(debounce_by=0.05):
                yield json.dumps({
                    "role": "assistant",
                    "timestamp": result.timestamp().isoformat(),
                    "content": delta
                }).encode("utf-8") + b"\n"
    return StreamingResponse(stream_messages(), media_type="text/plain")