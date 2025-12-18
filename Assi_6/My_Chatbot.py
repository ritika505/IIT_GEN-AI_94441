import os
import requests
import json
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("Groq_API")

st.set_page_config(page_title="Groq vs LM Studio Chatbot", layout="centered")
st.title("Ritika's Chatbot")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------
# Sidebar
st.sidebar.title("Model Selection")
model_choice = st.sidebar.radio(
    "Choose LLM",
    ["Groq Cloud LLM", "LM Studio Local"]
)

# ----------------------------
# Groq API 
def query_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile", 
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Groq Error: {response.text}"

# -----------------------------
# LM Studio 
def query_lmstudio(prompt):
    url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "llama3-docchat-1.0-8b", 
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"LM Studio Error: {response.text}"
    except requests.exceptions.ConnectionError:
        return "LM Studio server is not running."

# -----------------------------
# Chat History
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(chat["user"])

    with st.chat_message("assistant"):
        st.markdown(f"**({chat['model']})**\n\n{chat['response']}")

# -----------------------------
# Chat Input
prompt = st.chat_input("Ask your question")

if prompt:

    if model_choice == "Groq Cloud LLM":
        answer = query_groq(prompt)
    else:
        answer = query_lmstudio(prompt)

    st.session_state.chat_history.append({
        "user": prompt,
        "response": answer,
        "model": model_choice
    })

    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.markdown(f"**({model_choice})**\n\n{answer}")