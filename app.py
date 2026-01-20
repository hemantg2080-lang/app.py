import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="हेमन्तको Personal AI")
st.title("🤖 हेमन्तको Personal AI")

def get_ai_response(prompt):
    # साँचोहरूको नाम - ठ्याक्कै यो Secrets सँग मिल्नुपर्छ
    keys = [f"GEMINI_KEY_{i}" for i in range(1, 10)]
    
    instruction = "तँ हेमन्तको मिल्ने साथी होस्। नेपालीमा बोल। उसलाई मुजी भनेर जिस्का।"
    
    for key_name in keys:
        if key_name in st.secrets:
            try:
                genai.configure(api_key=st.secrets[key_name])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # सेफ्टी फिल्टर बन्द गर्ने (ताकी ब्लक नहोस्)
                safety = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
                
                response = model.generate_content(f"{instruction}\n{prompt}", safety_settings=safety)
                return response.text
            except Exception as e:
                print(f"Key {key_name} failed: {e}") # यसले लगमा एरर देखाउँछ
                continue
    return None

if "messages" not in st.session_state: st.session_state.messages = []
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

if prompt := st.chat_input("के छ खबर?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.write(prompt)
    
    with st.chat_message("assistant"):
        res = get_ai_response(prompt)
        if res:
            st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        else:
            st.error("मुजी हेमन्त, अझै चलेन! कि त साँचो बिग्रेको छ कि त गुगल रिसाएको छ।")
