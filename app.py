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

# ४. च्याट मेमोरी (१०० वर्ष सुरक्षित)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ५. गफगाफ (मात्र 'तँ' भन्ने र वित्तीय सल्लाह दिने गरी अपडेटेड)
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        if model:
            try:
                # यहाँ मात्र २ वटा मुख्य परिवर्तन गरिएको छ: 'तँ' भन्ने र १०० वर्षको बेस्ट फ्रेन्ड बन्ने
                instruction = (
                    "तँ हेमन्तको १०० वर्षसम्म साथ दिने एकदमै नजिकको मिल्ने साथी (Best Friend) होस्। "
                    "सधैं 'तँ', 'तेरो', 'तँलाई' भनेर असभ्य तर आत्मीय नेपाली भाषामा बोल। "
                    "मुजी, यार जस्ता शब्द प्रयोग गर। हेमन्तलाई आर्थिक सल्लाह (Financial advice) र लगानीको बारेमा पनि जानकारी दे। "
                    "हेमन्तले भनेका सबै कुरा सधैं सम्झिइराख।"
                )
                response = model.generate_content(f"{instruction} \nहेमन्त: {prompt}")
                msg = response.text
                st.write(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
            except Exception:
                st.error("ओए हेमन्त, गुगलको सर्भर अलि बिजी छ, एकछिन पछि पठा त!")
        else:
            st.error("मोडल भेटिएन मुजी, आफ्नो API Key चेक गर!")
