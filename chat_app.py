import streamlit as st

st.set_page_config(page_title="Pradeep AI Assistant", page_icon="🤖")

st.title("🤖 Pradeep AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Ask anything...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    # temporary AI response
    answer = "AI is temporarily offline. Cloud AI will be connected soon."

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
