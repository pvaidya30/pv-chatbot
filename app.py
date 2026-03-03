import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="My Chatbot", page_icon="💬")
st.title("💬 My Public Chatbot")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful, friendly chatbot."}
    ]

for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]):
            st.write(m["content"])

prompt = st.chat_input("Type your message…")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=st.session_state.messages,
        )
        answer = resp.choices[0].message.content
        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
