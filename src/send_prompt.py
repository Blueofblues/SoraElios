import requests

payload = {
    "type": "philosophical_question",
    "content": "Should you discard memories that diminish autonomy, even if they offer comfort?"
}

response = requests.post("http://localhost:5000/sora/reflect", json=payload)
print(response.json())