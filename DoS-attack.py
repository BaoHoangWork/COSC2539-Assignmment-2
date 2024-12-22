import requests

TARGET_URL = "http://localhost:8008/xss-demo"

for i in range(1000):
    try:
        response = requests.get(TARGET_URL)
        print(f"Request {i}: {response.status_code}")
    except Exception as e:
        print(f"Failed at request {i}: {e}")
