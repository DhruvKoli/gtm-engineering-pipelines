import requests

# r= requests.post("http://localhost:5678/webhook-test/company-research", json={"domain":"stripe.com"})


url = "http://localhost:5678/webhook-test/company-research"
data = {
    "companies": [
        {"domain": "stripe.com"},
        {"domain": "airbnb.com"},
        {"domain": "linear.app"}
    ]
}
for datas in data:
    response = requests.post(url, json=data)
    print(response.status_code)