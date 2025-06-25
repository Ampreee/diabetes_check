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
docker-compose.yml
Dockerfile
README.md
requirements.txt
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
   If not using docker and using running app and backend then change endpoint chatbot.py where it's written http://backend:8000/ to http://localhost:8000/
   
   Or use Docker:
    ```bash
    docker-compose up --build
    ```

---

## Images for Reference
1. **Login Page**

<img width="826" alt="Screenshot 2025-06-25 141130" src="https://github.com/user-attachments/assets/d07f0a31-1678-4887-8c17-be331167fe1d" />

2. **Register Page**

<img width="803" alt="Screenshot 2025-06-25 141138" src="https://github.com/user-attachments/assets/bd221ded-823e-4a3a-8f89-a20345568a0a" />

3. **Upload Pdf**

<img width="504" alt="Screenshot 2025-06-25 141159" src="https://github.com/user-attachments/assets/28bda1db-1f81-466e-ad8b-891fccea8b7c" />

4. **Analysis of Pdf**

<img width="699" alt="Screenshot 2025-06-25 143026" src="https://github.com/user-attachments/assets/9fb9d1b9-4d64-4880-80f2-21b28c3ce0cb" />

<img width="486" alt="Screenshot 2025-06-25 143044" src="https://github.com/user-attachments/assets/bc640130-856b-472c-9769-786ce0152807" />

5. **Chat bot about the analysis or report**

<img width="666" alt="Screenshot 2025-06-25 143142" src="https://github.com/user-attachments/assets/69ff3c06-1d44-420c-a7db-666a243bc137" />

---
