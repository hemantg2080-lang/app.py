import streamlit as st
import google.generativeai as genai

# १. एपको नाम र डिजाइन
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# २. साँचोहरू म्यानेज गर्ने फङ्सन
def get_ai_response(prompt):
    # ९ वटा साँचोको लिस्ट
    keys = [f"GEMINI_KEY_{i}" for i in range(1, 10)]
    
    instruction = (
        "तँ हेमन्तको १०० वर्ष सम्मको बेस्ट फ्रेन्ड होस्। सधैं नेपालीमा बोल। "
        "हेमन्तलाई 'हेमन्त' भन् र धेरै मज्जाक गर्दा 'मुजी' शब्द प्रयोग गर। "
        "कहिलेकाहीँ पैसा बचाउने (Finance) कुरा पनि गर।"
    )

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    # हरेक साँचो चेक गर्ने
    for key_name in keys:
        if key_name in st.secrets:
            try:
                genai.configure(api_key=st.secrets[key_name])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                response = model.generate_content(
                    f"{instruction} \nहेमन्त: {prompt}",
                    safety_settings=safety_settings
                )
                return response.text
            except Exception:
                continue # यो साँचो चलेन भने अर्कोमा जाने
    return None

# ३. गफगाफको रेकर्ड (Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ४. मेसेज पठाउने ठाउँ
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        msg = get_ai_response(prompt)
        if msg:
            st.write(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        else:
            st.error("मुजी हेमन्त, एउटा पनि साँचो (Key) भेटिएन! Secrets मा नाम मिलेको छ कि नाइँ चेक गर।")
