import streamlit as st
import google.generativeai as genai
import time

# १. एप सेटअप
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# २. मास्टर रिट्राइ र की-स्विचर फङ्सन
def get_ai_response(prompt):
    # सबै ९ वटा साँचोहरू
    keys = [
        "GEMINI_KEY_1", "GEMINI_KEY_2", "GEMINI_KEY_3",
        "GEMINI_KEY_4", "GEMINI_KEY_5", "GEMINI_KEY_6",
        "GEMINI_KEY_7", "GEMINI_KEY_8", "GEMINI_KEY_9"
    ]
    
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

    # हरेक साँचोलाई पालैपालो प्रयास गर्ने
    for key_name in keys:
        if key_name in st.secrets:
            try:
                genai.configure(api_key=st.secrets[key_name])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # रेट लिमिटबाट बच्न सानो विश्राम
                time.sleep(0.5)
                
                response = model.generate_content(
                    f"{instruction} \nहेमन्त: {prompt}",
                    safety_settings=safety_settings
                )
                return response.text
            except Exception as e:
                # यदि यो साँचो चलेन भने अर्कोमा जाने
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
                st.error("ओए हेमन्त, यति धेरै साँचो हुँदा पनि गुगलले पत्याएन मुजी! १ मिनेट पछि ट्राइ गर।")
