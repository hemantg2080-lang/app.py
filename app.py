import streamlit as st
from groq import Groq

# १. पेज सेटअप
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# २. Groq API Key तान्ने (Streamlit Secrets बाट)
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("हेमन्त, Streamlit Secrets मा GROQ_API_KEY हाल मुजी!")
    st.stop()

# ३. च्याट मेमोरी (१०० वर्षसम्म सम्झिने गरी)
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुराना म्यासेज देखाउने
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ४. हेमन्तको प्रश्न लिने र उत्तर दिने
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    # हेमन्तको म्यासेज सेभ गर्ने
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # मोडेललाई तेरो सर्त अनुसारको निर्देशन दिने
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": "You are Hemant's absolute best friend for the next 100 years. "
                                   "Always respond in Nepali. Remember every detail Hemant tells you "
                                   "to learn about him day by day. You are an expert in everything, "
                                   "especially financial matters and investment. Be helpful and loyal."
                    },
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile", # यो लेटेस्ट र चल्ने मोडेल हो
            )
            
            response_text = chat_completion.choices[0].message.content
            st.write(response_text)
            
            # एआईको म्यासेज सेभ गर्ने
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
        except Exception as e:
            st.error(f"ओए हेमन्त, यो सानो समस्या आयो: {e}")
