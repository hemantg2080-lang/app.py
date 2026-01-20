import streamlit as st
import google.generativeai as genai
import time

# १. एप सेटअप
st.set_page_config(page_title="हेमन्तको Personal AI", layout="centered")
st.title("🤖 हेमन्तको Personal AI")

# २. सुरक्षित चाबी
try:
    API_KEY = "AIzaSyCEfa1jZkFiPHOFR9cjlGoBYeHbLfNgTeQ" # तेरो साँचो
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("ओए हेमन्त, साँचो मिलेन मुजी!")

# ३. मोडल र सेफ्टी सेटिङ (ब्लक हुनबाट बच्न)
# यसले गर्दा तिम्रो मेसेजहरू बेकारमा रोकिँदैनन्
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
  {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
  {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
  {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings
)

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
        try:
            instruction = (
                "तँ हेमन्तको बेस्ट फ्रेन्ड होस्। नेपालीमा बोल। "
                "हेमन्तलाई 'हेमन्त' भन् र 'मुजी' भनेर जिस्का। "
                "कहिलेकाहीँ पैसाको (Financial) कुरा पनि गर।"
            )
            
            # ५ मेसेजमा ब्लक नहोस् भनेर सानो पर्खाइ (Delay)
            time.sleep(1) 
            
            response = model.generate_content(f"{instruction} \nहेमन्त: {prompt}")
            msg = response.text
            st.write(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
            
        except Exception as e:
            st.error("मुजी, गुगलले ब्लक गर्यो! १ मिनेट पर्खेर फेरि पठा त।")
