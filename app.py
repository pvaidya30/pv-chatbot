import streamlit as st
from openai import OpenAI
SYSTEM_PROMPT = """
You are PV Chatbot — friendly, concise, and practical.
If the user asks for harmful/illegal instructions, refuse and offer safe alternatives.
Ask 1 short follow-up question only when necessary.
"""

st.set_page_config(page_title="My Chatbot", page_icon="💬")
st.title("💬 My Public Chatbot")
st.caption("Built by Prachi (PV) • Streamlit + OpenAI demo chatbot")

if st.button("🧹 Clear chat"):
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.rerun()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
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
    messages_to_send = st.session_state.messages[-20:]  # last ~10 turns

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages_to_send,
    )
    answer = resp.choices[0].message.content
    st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

