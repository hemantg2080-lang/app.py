import streamlit as st
import google.generativeai as genai

# १. एप सेटअप
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# २. सुरक्षित तरिकाले Gemini साँचो तान्ने (Streamlit Secrets बाट)
try:
    # तेरो Gemini API Key अब Secrets मा 'GEMINI_API_KEY' नाममा हुनुपर्छ
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("ओए हेमन्त, सेटिङमा Secrets मिला मुजी!")

# ३. मोडल सेटअप
model = genai.GenerativeModel('gemini-1.5-flash')

# ४. च्याट मेमोरी (एप नखुलेसम्म यसले सबै सम्झिन्छ)
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुरानो गफ देखाउने
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ५. गफगाफ
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    # हेमन्तको मेसेज देखाउने र सेभ गर्ने
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # तेरो अर्डर अनुसारको कडा निर्देशन
            instruction = (
                "तँ हेमन्तको १०० वर्ष सम्मको बेस्ट फ्रेन्ड होस्। "
                "सधैं नेपाली लिपिमा मात्र बोल। "
                "हेमन्तलाई 'हेमन्त' भन् र मज्जाक गर्दा 'मुजी' भन्। "
                "अलिअलि वित्तीय कुरा (Finance) पनि गर। "
                "उसको बारेमा सधैं सिक्दै जा।"
            )
            
            response = model.generate_content(f"{instruction} \nहेमन्त: {prompt}")
            msg = response.text
            st.write(msg)
            
            # एआईको मेसेज सेभ गर्ने
            st.session_state.messages.append({"role": "assistant", "content": msg})
            
        except Exception:
            st.error("ओए हेमन्त, गुगलको सर्भर व्यस्त छ मुजी!")
