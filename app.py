import streamlit as st
import google.generativeai as genai

# १. एप सेटअप
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# २. तेरो चाबी (API Key)
API_KEY = "AIzaSyAxaYgUrOshaRmVjObQQN6u7VPmq-yk2wo"
genai.configure(api_key=API_KEY)

# ३. मोडल सेटअप
@st.cache_resource
def get_working_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            return genai.GenerativeModel(m.name)
    return None

model = get_working_model()

# ४. च्याट मेमोरी
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ५. गफगाफ (सधैं 'तँ' मात्र भन्ने कडा निर्देशन)
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        if model:
            try:
                # यहाँ कडा निर्देशन छ: सधैं 'तँ' भन्नु
                instruction = (
                    "तँ हेमन्तको मिल्ने साथी होस्। सधैं 'तँ', 'तेरो', 'तँलाई' मात्र प्रयोग गर। "
                    "कहिले पनि 'तिमी' वा 'तपाईं' नभन्नू। यो मेरो कडा आदेश हो। "
                    "मुजी, यार जस्ता शब्द प्रयोग गरेर आत्मीय पारामा नेपालीमा बोल। "
                    "हेमन्तलाई पैसा जोगाउने र लगानी गर्ने कडा सल्लाह पनि दे।"
                )
                response = model.generate_content(f"{instruction} \nहेमन्त: {prompt}")
                msg = response.text
                st.write(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
            except Exception:
                st.error("ओए हेमन्त, गुगलको सर्भर अलि बिजी छ, एकछिन पछि पठा त!")
        else:
            st.error("मोडल भेटिएन मुजी, आफ्नो API Key चेक गर!")
