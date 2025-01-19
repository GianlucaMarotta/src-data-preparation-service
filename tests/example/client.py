import requests
import json

url = "http://127.0.0.1:8000/prepare-data"

with open("request.json", "r") as f:
    data = json.load(f)

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.status_code, response.text)