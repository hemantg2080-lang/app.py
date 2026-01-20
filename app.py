# कोडको यो भागमा परिवर्तन गर:
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system", 
            "content": "You are Hemant's best friend for the next 100 years. Speak only in Nepali. Remember everything he tells you and learn about him day by day. You are an expert in everything in the world, including financial advice. Be supportive, loyal, and smart."
        },
        {"role": "user", "content": prompt}
    ],
    model="llama-3.3-70b-versatile",
)
