import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("Groq_API")
GEMINI_API_KEY = os.getenv("Gemini_API")
prompt = input("Ask any Question: ")


groq_url = "https://api.groq.com/openai/v1/chat/completions"
groq_headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}
groq_payload = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {"role": "user", "content": prompt}
    ]
}

start = time.time()
groq_response = requests.post(groq_url, json=groq_payload, headers=groq_headers)
groq_time = time.time() - start

groq_output = groq_response.json()["choices"][0]["message"]["content"]

gemini_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-3-flash-preview:generateContent?key={GEMINI_API_KEY}"

gemini_payload = {
    "contents": [
        {
            "parts": [
                {"text": prompt}
            ]
        }
    ]
}

start = time.time()
gemini_response = requests.post(gemini_url, json=gemini_payload)
gemini_time = time.time() - start

gemini_json = gemini_response.json()


if "candidates" in gemini_json:
    gemini_output = gemini_json["candidates"][0]["content"]["parts"][0]["text"]
else:
    gemini_output = "Gemini Error: " + str(gemini_json.get("error", "Unknown error"))


print("\n--- GROQ RESPONSE ---")
print(groq_output)
print(f"Time taken: {groq_time:.2f} seconds")

print("\n--- GEMINI RESPONSE ---")
print(gemini_output)
print(f"Time taken: {gemini_time:.2f} seconds")

print("\n--- SPEED COMPARISON ---")
if groq_time < gemini_time:
    print("Groq is faster ")
else:
    print("Gemini is faster ")
