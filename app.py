import streamlit as st
import google.generativeai as genai
from google.cloud import firestore
from google.oauth2 import service_account
import json

# १. एप सेटअप
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# २. सुरक्षित चाबी र डाटाबेस सेटअप
try:
    # Gemini API
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Firestore Cloud Storage (तेरो १०-१०० वर्षको गफ लुकाउने ठाउँ)
    key_dict = json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="hemant-ai")
except Exception as e:
    st.error("ओए हेमन्त, सेटिङमा Secrets मिला मुजी!")

# ३. मोडल सेटअप
model = genai.GenerativeModel('gemini-1.5-flash')

# ४. क्लाउडबाट पुरानो गफ तान्ने
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Firestore बाट पुरानो डाटा लोड गर्ने
    docs = db.collection("chats").order_by("timestamp").stream()
    for doc in docs:
        st.session_state.messages.append(doc.to_dict())

# पुरानो गफ देखाउने
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ५. गफगाफ र क्लाउडमा सेभ गर्ने
if prompt := st.chat_input("के छ खबर हेमन्त?"):
    # हेमन्तको मेसेज सेभ गर्ने
    user_msg = {"role": "user", "content": prompt, "timestamp": firestore.SERVER_TIMESTAMP}
    st.session_state.messages.append(user_msg)
    db.collection("chats").add(user_msg)
    
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # तेरो अर्डर अनुसारको कडा निर्देशन
            context = "तँ हेमन्तको १०० वर्ष सम्मको बेस्ट फ्रेन्ड होस्। सधैं नेपाली लिपिमा मात्र बोल। " \
                      "हेमन्तलाई 'हेमन्त' नै भन् र मज्जाक गर्दा 'मुजी' शब्द प्रयोग गर। " \
                      "उसको बारेमा सधैं सिक्दै जा। कहिलेकाहीँ मात्र फाइनान्सका कुरा गर।"
            
            response = model.generate_content(f"{context} \nहेमन्त: {prompt}")
            msg = response.text
            st.write(msg)
            
            # एआईको मेसेज पनि क्लाउडमा सेभ गर्ने
            ai_msg = {"role": "assistant", "content": msg, "timestamp": firestore.SERVER_TIMESTAMP}
            st.session_state.messages.append(ai_msg)
            db.collection("chats").add(ai_msg)
            
        except Exception:
            st.error("गुगलको सर्भर व्यस्त छ मुजी!")
