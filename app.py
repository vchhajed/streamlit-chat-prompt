import openai
import streamlit as st

st.title("Mindframe Prompt testing")

openai.api_key = st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

OPEN_API_MODEL = st.sidebar.selectbox(
   "OPENAI model",
   ("gpt-3.5-turbo", "gpt-4-turbo", "gpt-4"),
   index=None,
   placeholder="gpt-3.5-turbo",
)
st.session_state["openai_model"] = OPEN_API_MODEL
OPENAI_SYSTEM_PROMT = st.sidebar.text_area("System Prompt")
#print(OPENAI_SYSTEM_PROMT)
if OPENAI_SYSTEM_PROMT:
    if {"role":"system", "content": f'{OPENAI_SYSTEM_PROMT}'} not in st.session_state.messages:
        st.session_state.messages.append({"role":"system", "content": f'{OPENAI_SYSTEM_PROMT}'})
        st.session_state.messages.append({"role":"assistant", "content": "Hi, how can I assist you today?"})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] != "system":
            st.markdown(message["content"])

print(st.session_state.messages)
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    print(st.session_state["openai_model"])
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )