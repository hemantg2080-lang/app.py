import streamlit as st
import google.generativeai as genai

# १. एप सेटअप
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# २. तेरो नयाँ चाबी (API Key)
API_KEY = "AIzaSyCEfa1jZkFiPHOFR9cjlGoBYeHbLfNgTeQ"
genai.configure(api_key=API_KEY)

# ३. मोडल सेटअप
model = genai.GenerativeModel('gemini-1.5-flash')

# ४. च्याट मेमोरी (एप खुल्दासम्मको गफ याद राख्न)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ५. गफगाफ
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    # हेमन्तको मेसेज
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # तेरो नियम: 'हेमन्त' भन्ने, 'मुजी' भन्ने, अलिअलि फाइनान्स कुरा गर्ने
            instruction = (
                "तँ हेमन्तको मिल्ने साथी होस्। नेपालीमा मात्र बोल। "
                "हेमन्तलाई 'हेमन्त' भन् र धेरै मज्जाक गर्दा 'मुजी' भन्। "
                "कहिलेकाहीँ मात्र पैसा बचाउने (Finance) कुरा गर।"
            )
            
            response = model.generate_content(f"{instruction} \nहेमन्त: {prompt}")
            msg = response.text
            st.write(msg)
            
            # एआईको मेसेज सेभ गर्ने
            st.session_state.messages.append({"role": "assistant", "content": msg})
            
        except Exception:
            st.error("ओए हेमन्त, गुगलको सर्भर व्यस्त छ मुजी!")
