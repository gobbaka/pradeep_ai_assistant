import streamlit as st
import ollama
import time
import PyPDF2
import requests

st.set_page_config(page_title="Pradeep AI Assistant", page_icon="🤖", layout="wide")

st.title("🤖 Pradeep AI Assistant")

# ---------- SIDEBAR ----------
with st.sidebar:

    st.header("⚙ Tools")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    uploaded_file = st.file_uploader("Upload document", type=["txt","pdf"])

    web_search = st.checkbox("Enable Web Search")

    st.markdown("---")

    if "messages" in st.session_state:
        st.write("💬 Messages:", len(st.session_state.messages))

# ---------- MEMORY ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- FILE READING ----------
file_text = ""

if uploaded_file:

    if uploaded_file.type == "text/plain":
        file_text = uploaded_file.read().decode("utf-8")

    elif uploaded_file.type == "application/pdf":

        reader = PyPDF2.PdfReader(uploaded_file)

        for page in reader.pages:
            file_text += page.extract_text()

    st.success("Document loaded")

# ---------- SHOW CHAT ----------
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

        if msg["role"] == "assistant":
            st.button("📋 Copy", key=msg["content"])

# ---------- USER INPUT ----------
prompt = st.chat_input("Ask anything...")

if prompt:

    # Add document context
    if file_text:
        prompt = f"""
Use this document to help answer.

DOCUMENT:
{file_text}

QUESTION:
{prompt}
"""

    # Optional web search
    if web_search:

        try:

            r = requests.get(
                "https://api.duckduckgo.com/",
                params={
                    "q": prompt,
                    "format": "json"
                }
            )

            data = r.json()

            if data.get("AbstractText"):
                prompt += f"\n\nWeb info: {data['AbstractText']}"

        except:
            pass

    st.session_state.messages.append({
        "role":"user",
        "content":prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

# ---------- AI RESPONSE ----------
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":

    with st.chat_message("assistant"):

        placeholder = st.empty()

        placeholder.write("⏳ Thinking...")

        try:

            response = ollama.chat(
                model="tinyllama",
                messages=st.session_state.messages
            )

            answer = response["message"]["content"]

        except Exception as e:

            answer = f"AI Error: {e}"

        placeholder.empty()

        # streaming effect
        streamed = ""

        for word in answer.split():

            streamed += word + " "

            placeholder.markdown(streamed)

            time.sleep(0.02)

    st.session_state.messages.append({
        "role":"assistant",
        "content":answer
    })