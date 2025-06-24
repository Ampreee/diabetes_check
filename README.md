# Diabetes-Check: AI Health Assistant

## Overview

**Diabetes-Check** is a Streamlit-based web application that helps flag likely cases of Type 2 diabetes from uploaded clinical evidence. Users can authenticate (email/password or Google), upload medical records (PDFs, images, text), receive an AI-powered diabetes risk analysis, and then chat with an integrated assistant to ask follow-up questions about their results.

---

## Features

- **User Authentication:** Register/login via email/password or Google OAuth.
- **Upload Clinical Evidence:** Accepts PDF, JPG, PNG, CSV, and TXT files of health records or lab reports.
- **Instant AI Analysis:** Uses Pydantic-AI and OpenAI GPT-4o Mini for robust, explainable analysis of Type 2 diabetes risk.
- **Interactive Chatbot:** Ask context-aware questions about your analysis or uploaded records.
- **Interpretability:** Returns a human-readable summary, including key factors influencing the risk score.
- **Modern Stack:** Fast integration and validation with Pydantic-AI, seamless GPT-4o Mini responses, and Streamlit UI.

---

## How It Works

1. **Login/Register:**  
   Access the app with your credentials or Google account.
2. **Upload Record:**  
   Upload your medical record (PDF, image, or text file). The app processes and analyzes your data.
3. **See Analysis:**  
   Instantly view a probability score for Type 2 diabetes, with a concise explanation of contributing factors.
4. **Chat with AI:**  
   Ask follow-up questions about your analysis or health record. The AI chatbot uses the analysis context to provide detailed, relevant answers.

---

## Project Structure

```
src/
    api.py
    app.py             
    auth.py             
    chatbot.py   
    prompts.py           
.env.example
.gitignore
Dockerfile
docker-compose.yml
requirements.txt
README.md
```

---

## Setup & Running Locally

1. **Clone the Repository**
    ```bash
    git clone <your-repo-url>
    cd diabetes-check
    ```

2. **Set up environment variables**
    - Add keys in .env same as given in .env.example

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the App**
    ```bash
    streamlit run src/app.py
    ```
   For Backend
    ```bash
    uvicorn src.api:app --reload
    ```
   If using backend then change endpoint chatbot.py where it's written http://backend:8000/ to http://localhost:8000/
   
   Or use Docker:
    ```bash
    docker-compose up --build
    ```

---

