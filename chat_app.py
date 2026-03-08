import streamlit as st
from groq import Groq

st.set_page_config(page_title="Pradeep AI Assistant", page_icon="🤖")

st.title("🤖 Pradeep AI Assistant")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Ask anything...")

if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=st.session_state.messages
        )

        answer = response.choices[0].message.content
        st.write(answer)

    st.session_state.messages.append({"role":"assistant","content":answer})
