import streamlit as st
import google.generativeai as genai

# १. एप सेटअप
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# २. सुरक्षित तरिकाले चाबी तान्ने (Secrets बाट)
# अब कोडमा साँचो राख्नु पर्दैन
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("ओए हेमन्त, साँचो (API Key) सेटिङमा हालिस् त?")

# ३. उपलब्ध मोडल खोज्ने
@st.cache_resource
def get_working_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return genai.GenerativeModel(m.name)
    except:
        return None
    return None

model = get_working_model()

# ४. च्याट मेमोरी
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ५. गफगाफ
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        if model:
            try:
                response = model.generate_content(f"तपाईं हेमन्तको मिल्ने साथी हो। नेपालीमा उत्तर दिनुहोस्। हेमन्त: {prompt}")
                msg = response.text
                st.write(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
            except Exception:
                st.error("गुगलको सर्भर व्यस्त छ, १ मिनेट पछि फेरि पठा त!")
        else:
            st.error("सेटिङमा API Key मिलेन मुजी!")
