import streamlit as st
from auth import (
    register_user, authenticate_user, get_user_by_email,
    register_google_user
)
from chatbot import ask_ai, analyse_file
import os
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv
import json

load_dotenv()

st.set_page_config(page_title="Diabetes-Check", page_icon="🩺")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8501"
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

# Session state setup
for key in ["authenticated", "user_email", "username", "chat_history", "uploaded_text"]:
    if key not in st.session_state:
        st.session_state[key] = False if key == "authenticated" else None if key != "chat_history" else []

def get_google_auth_url():
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account"
    }
    return f"{AUTH_URL}?{urlencode(params)}"

def get_google_token(code):
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    r = requests.post(TOKEN_URL, data=data)
    return r.json()

def get_google_user_info(token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(USER_INFO_URL, headers=headers)
    return r.json()

def login_ui():
    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = authenticate_user(email, password)
        if user:
            st.session_state.authenticated = True
            st.session_state.user_email = user[2]
            st.session_state.username = user[1]
            st.success("Logged in!")
        else:
            st.error("Invalid credentials!")
    st.markdown("---")
    st.markdown("Or login with Google:")
    google_login_url = get_google_auth_url()
    st.markdown(f'<a href="{google_login_url}" target="_self"><button>Login with Google</button></a>', unsafe_allow_html=True)

def register_ui():
    st.header("Register")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if not username or not email or not password:
            st.warning("Please fill all fields.")
        elif get_user_by_email(email):
            st.warning("Email already registered.")
        else:
            if register_user(username, email, password):
                st.success("Registration successful! Please login.")
            else:
                st.error("Registration failed.")

def logout_ui():
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.session_state.username = None
        st.session_state.chat_history = []
        st.session_state.uploaded_text = None
        st.rerun()

def handle_google_callback():
    query_params = st.query_params
    if "code" in query_params:
        code = query_params["code"]
        if isinstance(code, list):
            code = code[0]
        token_data = get_google_token(code)
        access_token = token_data.get("access_token")
        if access_token:
            user_info = get_google_user_info(access_token)
            email = user_info.get("email")
            name = user_info.get("name")
            google_id = user_info.get("id")
            register_google_user(email, name, google_id)
            st.session_state.authenticated = True
            st.session_state.user_email = email
            st.session_state.username = name
            st.query_params.clear()
            st.success(f"Logged in as {name} via Google.")
            return True
        else:
            st.error("Google login failed.")
            return False
    return False

def file_upload_and_analysis_ui():
    st.subheader("Upload Health Record for Diabetes Check")
    uploaded_file = st.file_uploader("Upload file (PDF, image, or text)", type=["pdf", "jpg", "jpeg", "png", "bmp", "tiff", "csv", "txt"])
    if uploaded_file:
        result, extracted_text = analyse_file(uploaded_file, return_text=True)  
        st.session_state.uploaded_text = extracted_text

def ai_chat_ui():
    st.subheader("Ask Questions About Your Uploaded Data")
    if not st.session_state.uploaded_text:
        st.info("Upload a file first to chat about it.")
        return
    user_input = st.text_input("Ask a question:")
    if st.button("Send") and user_input.strip():
        answer = ask_ai(user_input, st.session_state.uploaded_text, st.session_state.chat_history)
        st.session_state.chat_history.append((user_input, answer))
        st.markdown(f"**You:** {user_input}")
        st.markdown(f"**AI:** {answer}")

    if st.session_state.chat_history:
        st.markdown("### Previous Q&A")
        for q, a in st.session_state.chat_history:
            st.markdown(f"**You:** {q}")
            st.markdown(f"**AI:** {a}")

def main():
    st.title("Diabetes-Check: AI Health Assistant")

    if handle_google_callback():
        pass

    if st.session_state.authenticated:
        st.subheader(f"Hello, {st.session_state.username}!")
        logout_ui()
        st.markdown("---")
        file_upload_and_analysis_ui()
        st.markdown("---")
        ai_chat_ui()
    else:
        choice = st.radio("Choose", ["Login", "Register"])
        if choice == "Login":
            login_ui()
        else:
            register_ui()

if __name__ == "__main__":
    main()
