import requests

url = "http://localhost:5678/webhook-test/new-lead"
data = {
    "name": "Rahul Sharma",
    "email": "rahul@example.com",
    "company": "TechNova",
    "source": "Website"
}

r = requests.post(url, json=data)
print(r.status_code)