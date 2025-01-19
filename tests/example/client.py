import requests
import json

url = "http://localhost:8000/prepare-data"
filename = "request_copy.json"

with open(filename, "r") as f:
    data = json.load(f)

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.status_code, response.text)