import requests, json
url = "http://127.0.0.1:8000/predict"
data = {
    "question": "What is the largest planet in our solar system?",
    "options": ["Earth", "Jupiter", "Mars", "Venus"]
}
r = requests.post(url, json=data)
print(r.status_code)
try:
    print(r.json())
except:
    print(r.text)