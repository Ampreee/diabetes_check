# api.py
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, AsyncGenerator
from pydantic_ai import Agent
from pydantic_ai.messages import TextPart,ModelResponse
from datetime import datetime, timezone
import json
import io
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract

app = FastAPI()

# CORS for Streamlit
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

@app.post("/chat/")
async def post_chat(
    prompt: Annotated[str, Form()],
    context: Annotated[str, Form()],
):
    full_prompt = f"""
You are an AI medical assistant. Given the following patient data:

{context}

Answer the question: {prompt}
"""

    async def stream_messages() -> AsyncGenerator[bytes, None]:
        # 1. Stream the user's message (optional for frontend history)
        yield (
            json.dumps({
                "role": "user",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "content": prompt,
            }).encode("utf-8") + b"\n"
        )

        # 2. Run the agent streaming loop
        async with agent.run_stream(full_prompt) as result:
            async for delta in result.stream(debounce_by=0.05):
                # model_response = ModelResponse(parts=[TextPart(delta)], timestamp=result.timestamp())
                # chat_msg = {
                #     "role": "assistant",
                #     "timestamp": result.timestamp().isoformat(),
                #     "content": delta,
                # }
                # yield json.dumps(chat_msg).encode("utf-8") + b"\n"
                yield json.dumps({
                    "role": "assistant",
                    "timestamp": result.timestamp().isoformat(),
                    "content": delta  # ✅ only new token
                }).encode("utf-8") + b"\n"

    return StreamingResponse(stream_messages(), media_type="text/plain")