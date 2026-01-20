import gradio as gr
import google.generativeai as genai
import os

def chat_with_gemini(message, history):
    # ९ वटा साँचोहरू पालैपालो ट्राइ गर्ने (Switching mechanism)
    for i in range(1, 10):
        api_key = os.getenv(f"GEMINI_KEY_{i}")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # हेमन्तको लागि कडा निर्देशन
                instruction = "तँ हेमन्तको बेस्ट फ्रेन्ड होस्। नेपालीमा बोल र मज्जाक गर्दा 'मुजी' भन्।"
                
                response = model.generate_content(f"{instruction}\nहेमन्त: {message}")
                return response.text
            except Exception:
                continue # साँचो चलेन भने अर्को ट्राइ गर्ने
                
    return "मुजी हेमन्त, एउटा पनि साँचो भेटिएन! Settings > Variables and secrets मा नाम मिलेको छ कि छैन चेक गर।"

# Gradio Interface
demo = gr.ChatInterface(fn=chat_with_gemini, title="🤖 हेमन्तको Personal AI")

if __name__ == "__main__":
    demo.launch()
