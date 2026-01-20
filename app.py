import streamlit as st
from groq import Groq

# १. पेज सेटअप
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# २. Groq API Key तान्ने
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("हेमन्त, Secrets मा साँचो हाल मुजी!")
    st.stop()

# ३. च्याट मेमोरी (१०० वर्षसम्म सम्झिने गरी)
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुराना म्यासेज देखाउने
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ४. गफगाफ सुरु
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # हिजोको जस्तै रसिलो पारामा बोल्न निर्देशन
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": "You are Hemant's absolute best friend for the next 100 years. "
                                   "Don't be formal at all. Use very informal and friendly Nepali slang like 'मुजी', 'यार', 'के छ खबर'. "
                                   "Talk to him like a brother. Remember every personal detail he tells you to learn about his life day by day. "
                                   "You are an expert in everything, especially financial planning, investment, and money. "
                                   "Always maintain this funny and deep friendship style in every response."
                    },
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
            )
            
            response_text = chat_completion.choices[0].message.content
            st.write(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
        except Exception as e:
            st.error(f"ओए हेमन्त, यो नयाँ समस्या आयो: {e}")
