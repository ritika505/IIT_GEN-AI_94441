# 3. ⁠Use LM studio on your laptop. Explore its UI.
import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()
api_key = "dummy-key"
url = "http://127.0.0.1:1234/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

while True:
    user_prompt = input("Ask anything: ")
    if user_prompt == "exit":
        break
    req_data = {
        "model": "microsoft/phi-4-mini-reasoning",
        "messages": [
            { "role": "user", "content": user_prompt }
        ]
    }
    time1 = time.perf_counter()
    response = requests.post(url, json=req_data, headers=headers)
    time2 = time.perf_counter()
    print("Status:", response.status_code)
    # print(response.json())
    resp = response.json()
    print(resp["choices"][0]["message"]["content"])
