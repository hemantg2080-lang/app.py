import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

def get_ai_response(prompt):
    # ९ वटा साँचोहरू चेक गर्ने
    for i in range(1, 10):
        key_name = f"GEMINI_KEY_{i}"
        
        if key_name in st.secrets:
            try:
                # साँचो कनेक्ट गर्ने
                genai.configure(api_key=st.secrets[key_name])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # मज्जाक ब्लक नहुने सेटिङ
                safety = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
                
                instruction = "तँ हेमन्तको बेस्ट फ्रेन्ड होस्। नेपालीमा बोल र उसलाई मुजी भनेर जिस्का।"
                response = model.generate_content(f"{instruction}\n{prompt}", safety_settings=safety)
                return response.text
            except Exception:
                continue # यो साँचो चलेन भने अर्कोमा जाने
    return None

# च्याट ईतिहास
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

if prompt := st.chat_input("के छ खबर हेमन्त?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("एकछिन रोक् है मुजी..."):
            res = get_ai_response(prompt)
            if res:
                st.write(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            else:
                st.error("मुजी हेमन्त, एउटा पनि साँचो (Key) भेटिएन! Secrets मा नाम मिलेको छ कि नाइँ चेक गर्।")
