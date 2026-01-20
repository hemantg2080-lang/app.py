import streamlit as st
from groq import Groq

st.set_page_config(page_title="हेमन्तको Super AI", layout="centered")
st.title("🚀 हेमन्तको Super AI")

if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("हेमन्त, Secrets मा साँचो हाल मुजी!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("के छ खबर हेमन्त?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are Hemant's best friend. Answer in Nepali."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192",
            )
            msg = chat_completion.choices[0].message.content
            st.write(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            st.error(f"Error: {e}")
