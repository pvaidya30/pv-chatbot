import streamlit as st
from openai import OpenAI

SYSTEM_PROMPT = """
You are PV Chatbot — friendly, concise, and practical.
If the user asks for harmful/illegal instructions, refuse and offer safe alternatives.
Ask 1 short follow-up question only when necessary.
"""

st.set_page_config(page_title="PV Chatbot", page_icon="💬")
st.title("💬 PV Chatbot")
st.caption("Built by Prachi (PV) • Streamlit + OpenAI demo chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Clear chat button
if st.button("🧹 Clear chat"):
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.rerun()

# OpenAI client (API key stored in Streamlit Secrets)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Display chat history (skip system)
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]):
            st.write(m["content"])

# User input
prompt = st.chat_input("Type your message…")
if prompt:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        messages_to_send = st.session_state.messages[-20:]  # last ~10 turns

        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages_to_send,
        )
        answer = resp.choices[0].message.content
        st.write(answer)

    # Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": answer})
