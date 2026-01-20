import streamlit as st
import google.generativeai as genai

# १. एप सेटअप
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# २. तेरो चाबी (API Key) - यसलाई मात्र अपडेट गरिएको छ
API_KEY = "AIzaSyAxaYgUrOshaRmVjObQQN6u7VPmq-yk2wo"
genai.configure(api_key=API_KEY)

# ३. उपलब्ध मोडल खोज्ने तरिका
@st.cache_resource
def get_working_model():
    # एरर नआओस् भनेर सिधै एउटा चल्ने मोडल नाम दिइएको छ
    return genai.GenerativeModel('gemini-1.5-flash')

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
                st.error("ओए हेमन्त, गुगलको सर्भर व्यस्त छ, १ मिनेट पछि फेरि पठा त!")
        else:
            st.error("मोडल फेला परेन। आफ्नो API Key चेक गर!")
