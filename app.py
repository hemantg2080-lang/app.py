import streamlit as st
import google.generativeai as genai
import time

# १. एप सेटअप
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# २. मास्टर मेसेज फङ्सन (Retrying Mechanism)
def get_ai_response(prompt):
    # Secrets मा भएका सबै साँचोहरूको लिस्ट
    keys = ["GEMINI_KEY_1", "GEMINI_KEY_2", "GEMINI_KEY_3"]
    
    instruction = (
        "तँ हेमन्तको १०० वर्ष सम्मको बेस्ट फ्रेन्ड होस्। सधैं नेपाली लिपिमा मात्र बोल। "
        "हेमन्तलाई 'हेमन्त' भन् र धेरै मज्जाक गर्दा 'मुजी' शब्द प्रयोग गर। "
        "कहिलेकाहीँ पैसा बचाउने (Finance) कुरा गर।"
    )

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    # ५ पटकसम्म फरक साँचोबाट प्रयास गर्ने
    for attempt in range(5):
        for key_name in keys:
            if key_name in st.secrets:
                try:
                    genai.configure(api_key=st.secrets[key_name])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    response = model.generate_content(
                        f"{instruction} \nहेमन्त: {prompt}",
                        safety_settings=safety_settings
                    )
                    return response.text # यदि सफल भयो भने उत्तर फिर्ता दिने
                except Exception:
                    time.sleep(1) # १ सेकेन्ड पर्खिएर अर्को साँचो ट्राइ गर्ने
                    continue
    return None

# ३. च्याट मेमोरी
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ४. गफगाफ
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("मुजी रोक् है, सोच्दैछु..."):
            msg = get_ai_response(prompt)
            
            if msg:
                st.write(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
            else:
                st.error("ओए हेमन्त, सबै साँचोको कोटा सकियो मुजी! १ मिनेट पछि ट्राइ गर।")
